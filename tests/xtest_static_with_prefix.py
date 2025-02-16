"""
This shows how to use the CFFI static (API) binding.  It should be fast and code be as close as possible to original
C code.
"""

import raylib as rl

rl.InitWindow(800, 450, b"Raylib static binding test with prefix")
rl.SetTargetFPS(60)

camera = rl.ffi.new("struct Camera3D *", [[18.0, 16.0, 18.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], 45.0, 0])
image = rl.LoadImage(b"examples/models/resources/heightmap.png")
texture = rl.LoadTextureFromImage(image)
mesh = rl.GenMeshHeightmap(image, [16, 8, 16])
model = rl.LoadModelFromMesh(mesh)
print(model.materials)  # SHOULD BE A pointer to a 'struct Material' but some is NULL pointer to 'Material' ?
model.materials.maps[rl.MATERIAL_MAP_ALBEDO].texture = texture

rl.UnloadImage(image)
rl.SetCameraMode(camera[0], rl.CAMERA_ORBITAL)

while not rl.WindowShouldClose():
    rl.UpdateCamera(camera)
    rl.BeginDrawing()
    rl.ClearBackground(rl.RAYWHITE)
    rl.BeginMode3D(camera[0])
    rl.DrawModel(model, (-8.0, 0.0, -8.0), 1.0, rl.RED)
    rl.DrawGrid(20, 1.0)
    rl.EndMode3D()
    rl.DrawText(b"This mesh should be textured", 190, 200, 20, rl.VIOLET)
    rl.EndDrawing()
rl.CloseWindow()
