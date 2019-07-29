bl_info = {
    "name": "Batch FBX Importer",
    "description": "Imports multiple fbx files in a folder.",
    "author": "Arda Hamamcıoğlu",
    "version": (0, 1, 2),
    "blender" : (2, 80, 0),
    "support": "COMMUNITY",
    "category": "Import-Export"
}

import bpy
from bpy import context
from bpy.props import (StringProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )
import os

class FbxImporterPanel(Panel):
    bl_idname = "OBJECT_PT_fbx_import_panel"
    bl_label = "Batch FBX Importer"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FBX Importer"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        row = layout.box()
        row.label(text="1)Select Folder Containing FBX Files:")
        
        row.prop(scn, "import_path",icon ='FILE_IMAGE')
        
        row = layout.box()
        row.label(text="2)Hit The Import Button To Import:")
        
        row.operator("object.batch_fbx_import")

class BatchFbxImport(Operator):
    bl_idname = "object.batch_fbx_import"
    bl_label = "FBX Batch Importer"
    import_dir = ""

    def execute(self,context):

        import_dir = bpy.path.abspath(context.scene.import_path)

        if not os.path.isdir(import_dir):
            raise Exception("No folder selected.")
            
        file_list = sorted(os.listdir(import_dir))
        fbx_list = [item for item in file_list if item.endswith('.fbx')]
        
        for item in fbx_list:
            path = os.path.join(import_dir,item)
            bpy.ops.import_scene.fbx(filepath=path)
        
        return{'FINISHED'}

def register():
    bpy.utils.register_class(FbxImporterPanel)
    bpy.utils.register_class(BatchFbxImport)
    bpy.types.Scene.import_path = bpy.props.StringProperty(name="Folder Path", default = "", description = "Navigate to the folder containing FBX files.", subtype = 'DIR_PATH')

def unregister():
    bpy.utils.unregister_class(FbxImporterPanel)
    bpy.utils.unregister_class(BatchFbxImport)
    del bpy.types.Scene.import_path

if __name__ == "__main__":
    register()