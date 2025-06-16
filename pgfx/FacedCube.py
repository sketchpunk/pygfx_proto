import wgpu
import pygfx as gfx
from pygfx.renderers.wgpu import (
    Binding,
    BaseShader,
    RenderMask,
    register_wgpu_render_function,
)


def facedCube():
    geo = gfx.box_geometry(1, 1, 1)
    mat = FacedCubeMaterial()  # gfx.MeshPhongMaterial(color="#336699", pick_write=True)
    mesh = gfx.Mesh(geo, mat)
    mesh.local.y = 0.5
    return mesh


class FacedCubeMaterial(gfx.Material):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@register_wgpu_render_function(gfx.WorldObject, FacedCubeMaterial)
class FacedCubeShader(BaseShader):
    type = "render"

    def get_bindings(self, wobject, shared):
        geometry = wobject.geometry
        material = wobject.material

        # Our only binding is a uniform buffer
        bindings = {
            0: Binding("u_stdinfo", "buffer/uniform", shared.uniform_buffer),
            1: Binding("u_wobject", "buffer/uniform", wobject.uniform_buffer),
            2: Binding("u_material", "buffer/uniform", material.uniform_buffer),
            3: Binding("s_indices", "buffer/read_only_storage", geometry.indices, "VERTEX"),
            4: Binding("s_positions", "buffer/read_only_storage", geometry.positions, "VERTEX"),
            5: Binding("s_normals", "buffer/read_only_storage", geometry.normals, "VERTEX"),
        }

        self.define_bindings(0, bindings)
        return {
            0: bindings,
        }

    def get_pipeline_info(self, wobject, shared):
        return {
            "primitive_topology": wgpu.PrimitiveTopology.triangle_list,
            "cull_mode": wgpu.CullMode.back,
        }

    def get_render_info(self, wobject, shared):
        n = wobject.geometry.indices.data.size
        return {
            "indices": (n, 1),
            "render_mask": RenderMask.opaque,
        }

    def get_code(self):
        # Here we put together the full (templated) shader code
        return """
        {$ include 'pygfx.std.wgsl' $}

        struct VertexInput {
            @builtin(vertex_index) vertex_index : u32,
        };

        @vertex
        fn vs_main(in: VertexInput) -> Varyings {
            // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            // Get Attributes
            let vertex_index = i32(in.vertex_index);
            let face_index = vertex_index / 3;
            var sub_index = vertex_index % 3;
            let ii = load_s_indices(face_index);
            let i0 = i32(ii[sub_index]);

            let pos = load_s_positions(i0);
            let norm = load_s_normals(i0);

            // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            let u_mvp    = u_stdinfo.projection_transform * u_stdinfo.cam_transform * u_wobject.world_transform;
            let position = u_mvp * vec4<f32>( pos, 1.0 );

            // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            var varyings: Varyings;
            varyings.position = vec4<f32>(position);

            // PATTERN
            // x 0, 1 -1  0,1
            // y 1, 1,-1  2,3
            // z 2, 1,-1, 4,5
            // abs(x) * 0 + max(-x,0)
            // abs(y) * 2 + max(-y,0)
            // abs(z) * 4 + max(-z,0)

            let colors: array<vec3<f32>, 6> = array<vec3<f32>, 6>(
                vec3<f32>( 0.9, 0.1, 0.1),       // +X Red
                vec3<f32>( 0.15, 0.05, 0.05),    // -X Alt Red
                vec3<f32>( 0.1, 0.9, 0.1),       // +Y Green
                vec3<f32>( 0.05, 0.15, 0.05),    // -Y Alt Green
                vec3<f32>( 0.1, 0.1, 1.0),       // +Z Blue
                vec3<f32>( 0.05, 0.05, 0.15)     // -Z Alt Blue
            );

            let vIdx = vec3<i32>(
                clamp( i32( round( norm.x ) ), -1, 1 ),
                clamp( i32( round( norm.y ) ), -1, 1 ),
                clamp( i32( round( norm.z ) ), -1, 1 )
            );

            let i: i32 = 
                ( abs( vIdx.x ) * 0 + max( -vIdx.x, 0 ) ) +
                ( abs( vIdx.y ) * 2 + max( -vIdx.y, 0 ) ) +
                ( abs( vIdx.z ) * 4 + max( -vIdx.z, 0 ) );

            varyings.color = vec3<f32>( colors[ i ] );    

            return varyings;
        }

        @fragment
        fn fs_main( varyings: Varyings ) -> FragmentOutput {
            var out: FragmentOutput;
            out.color = vec4<f32>(varyings.color, 1.0);
            return out;
        }
        """


# // The builtin write_pick templating variable should be used
# // to ensure picking info is only written in the appropriate render pass
# $$ if write_pick
# // 20 + 26 + 6 + 6 + 6 = 64
# out.pick = (
#     pick_pack(varyings.pick_id, 20) +
#     pick_pack(varyings.pick_idx, 26) +
#     pick_pack(u32(varyings.pick_coords.x * 64.0), 6) +
#     pick_pack(u32(varyings.pick_coords.y * 64.0), 6) +
#     pick_pack(u32(varyings.pick_coords.z * 64.0), 6)
# );
# $$ endif
