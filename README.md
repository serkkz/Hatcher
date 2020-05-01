# Hatcher 2.8

Egg exporter for blender 2.8

This plugin is just part of a broader concept. 
The plugin's goal is to provide an interface for editing geometry with maximum support for EGG format functions. 
But need to make changes to the EGG format to support materials from external files.
There is also an option to opt out of the EGG format instead .blend file. But to do this, I need to learn the basics of C++ coding.

## Concept

![Image alt](https://github.com/serkkz/Hatcher-2.8/blob/master/Diagram.png)


## Supported exporting
| Description            | Exporting  | 
|------------------------|:----------:|
| Meshes                 | Yes        |
| UV layers              | Yes        |
| Materials and textures | No         |
| Armature animation     | No         |
| ShapeKeys animation    | No         |
| NURBS                  | No         |
| Include Egg            | Yes        |
| Polygon name           | Yes        |
| Сollision name         | Yes        |
| Сollision mask         | Yes        |


## Supported functions
| Description                 | Functions  | 
|-----------------------------|:----------:|
| Calling the egg2bam utility | Yes        |
| Calling the pview utility   | Yes        |
| Configuring export paths    | Yes        |

## Installation

https://github.com/serkkz/Hatcher/wiki/Installation