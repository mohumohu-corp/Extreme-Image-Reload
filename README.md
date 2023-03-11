# Simple Auto Texture Reload Addon for Blender 3.3 or higher

- Supports both Regular and UDIM Texture reload.
- Extremely simple. There is only one button.
- Suitable for workflows where you can create high quality UDIM textures in illustration software such as Photoshop/Clipstudio and view the results in real-time in the Blender viewport. Using multiple UV maps in Blender, you can combine UDIM textures into one single final texture.

## How to Install

- Download zip file by pressing the green "Code" button on the master branch, then select the file in the Preferences window of Blender and install it.

## Reload Behaviour

- When textures set in blender materials are rewritten by external software, they are automatically reloaded by Blender and reflected in the ViewPort.
- There are three modes: Disabled, Enabled, and AnimEnabled. Only in AnimEnabled mode, textures are updated even during animation playback.

| State / Mode    | ![enabled](https://raw.githubusercontent.com/mohumohu-corp/ExtremeImageReload/images/off.png)Disabled | ![enabled](https://raw.githubusercontent.com/mohumohu-corp/ExtremeImageReload/images/enabled.png) Enabled | ![enabled](https://raw.githubusercontent.com/mohumohu-corp/ExtremeImageReload/images/anim_enabled.png)AnimEnabled |
|-----------------|-------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| Normal          | off                                                                                                   | on                                                                                                        | on                                                                                                                |
| During Playback | off                                                                                                   | off                                                                                                       | on                                                                                                                |

## Button Location

- There is a toggle button in the upper right corner of the 3D Viewport window.

![enabled](https://raw.githubusercontent.com/mohumohu-corp/ExtremeImageReload/images/location.png)


