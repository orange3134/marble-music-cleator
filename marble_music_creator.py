bl_info = {
    "name": "Marble Music Creator",
    "blender": (4, 0, 0),
    "category": "Object",
    "author": "orange3134",
    "version": (0, 0, 1),
    "description": "Auxiliary tools to simplify the creation of Marble music",
}

import bpy
import random
from math import radians
from mathutils import Vector
import numpy as np

# パネルクラス
class PREFAB_PT_panel(bpy.types.Panel):
    bl_label = "Marble Music Creator"
    bl_idname = "MMC_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Marble Music Creator'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # ターゲットオブジェクトとプレファブオブジェクトの選択
        layout.prop(scene, "target_object")
        layout.prop(scene, "prefab_object")
        layout.prop(scene, "collection_of_instance")
        layout.prop(scene, "position_offset")
        layout.prop(scene, "random_rotation_angle")
        
        # 配置ボタン
        layout.operator("object.duplicate_prefab")

@bpy.app.handlers.persistent
def get_target_velocity(scene):
    global target_object_velocity
    global target_object_current_position
    global target_object_last_position
    if 'target_object_last_position' not in globals():
        target_object_last_position = Vector((0, 0, 0))

    target_object = scene.target_object
    if target_object:
        bpy.context.view_layer.update()
        target_object_current_position = target_object.matrix_world.translation.copy()
        target_object_velocity = target_object_current_position - target_object_last_position
        target_object_last_position = target_object_current_position
        print(target_object_velocity)


# オペレータークラス
class PREFAB_OT_duplicate(bpy.types.Operator):
    bl_label = "Duplicate Prefab"
    bl_idname = "object.duplicate_prefab"
    bl_options = {'UNDO'}

    def execute(self, context):
        scene = context.scene
        target_object = scene.target_object
        prefab_object = scene.prefab_object
        position_offset = scene.position_offset
        random_rotation_angle = scene.random_rotation_angle
        collection_of_instance = scene.collection_of_instance
        new_prefab = None

        if not target_object or not prefab_object:
            self.report({'WARNING'}, "ターゲットオブジェクトとプレファブオブジェクトを選択してください")
            return {'CANCELLED'}

        # ターゲットオブジェクトの移動量ベクトルの計算
        move_vector = target_object_velocity.normalized()

        # 配置位置の計算
        position = target_object_current_position

        current_length = np.linalg.norm(move_vector)
        scale_factor = position_offset / current_length
        offset_vector = move_vector * scale_factor

        new_location = position + offset_vector

        # プレファブの複製と配置
        bpy.ops.object.select_all(action='DESELECT')  # 全てのオブジェクトの選択を解除
        prefab_object.select_set(True)
        bpy.context.view_layer.objects.active = prefab_object

        # 子オブジェクトを選択する
        for child in prefab_object.children:
            child.select_set(True)
        
        # 複製する
        bpy.ops.object.duplicate()

        # コレクションを変更
        if collection_of_instance is not None:
            for selected in bpy.context.selected_objects:
                collections = selected.users_collection
                for collection in collections:
                    if collection != bpy.context.scene.rigidbody_world.collection:
                        collection.objects.unlink(selected)
                collection_of_instance.objects.link(selected)

        # 複製されたオブジェクトを取得
        for selected in bpy.context.selected_objects:
            if selected.type == "EMPTY":
                new_prefab = selected
                break
        if new_prefab is None:
            new_prefab = bpy.context.selected_objects[0]

        new_prefab.location = new_location

        # プレファブオブジェクトの回転設定
        move_vector_angle = self.calc_vector_angle(Vector((0, 0, 1)), move_vector)
        if position.x - new_location.x > 0:
            move_vector_angle = -move_vector_angle

        print(move_vector_angle)
        new_prefab.rotation_euler.z = 0 
        new_prefab.rotation_euler.y = move_vector_angle + random.uniform(radians(random_rotation_angle), -radians(random_rotation_angle)) + radians(180) 
        
        return {'FINISHED'}
    
    def calc_vector_angle(self, v1, v2):
        cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        theta = np.arccos(cos_theta)
        return theta

# プロパティの登録
def register():
    bpy.utils.register_class(PREFAB_PT_panel)
    bpy.utils.register_class(PREFAB_OT_duplicate)
    bpy.types.Scene.target_object = bpy.props.PointerProperty(
        name="Target Object",
        type=bpy.types.Object,
        description="ターゲットオブジェクトを選択してください"
    )
    bpy.types.Scene.prefab_object = bpy.props.PointerProperty(
        name="Prefab Object",
        type=bpy.types.Object,
        description="プレファブオブジェクトを選択してください"
    )
    bpy.types.Scene.collection_of_instance = bpy.props.PointerProperty(
        name="Collection of Instance",
        type=bpy.types.Collection,
        description="複製したオブジェクトを格納するコレクション"
    )
    bpy.types.Scene.position_offset = bpy.props.FloatProperty(
        name="Position Offset",
        default=0.3,
        description="ターゲットオブジェクトからのオフセット距離"
    )
    bpy.types.Scene.random_rotation_angle = bpy.props.FloatProperty(
        name="Random Rotation Angle",
        default=30.0,
        description="プレファブオブジェクトのY軸回転角度"
    )

    bpy.app.handlers.frame_change_post.append(get_target_velocity)

def unregister():
    bpy.utils.unregister_class(PREFAB_PT_panel)
    bpy.utils.unregister_class(PREFAB_OT_duplicate)
    del bpy.types.Scene.target_object
    del bpy.types.Scene.prefab_object
    del bpy.types.Scene.collection_of_instance
    del bpy.types.Scene.position_offset

    bpy.app.handlers.frame_change_post.remove(get_target_velocity)

if __name__ == "__main__":
    register()
