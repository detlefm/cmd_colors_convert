# cmd_colors_convert
Regfile generator for cmd and bash colors

Inspired from this issue ( https://github.com/Microsoft/BashOnWindows/issues/1175 ) 
I want to find out how colors are working in the terminals of the windows world like cmd, bash and powershell.
Are they stored in the registry? Are they stored in the shortcut?

For accessing the linux subsystem I personally use wsltty which is based on mintty, because it is easy to change colors to my needs. But for bash, powershell and cmd to get colors you have to go through a click and error path to make "your" colors.


## Properties store places

There are at least 5 programs depending on the registry console branch.

cmd.exe ( 32-bit and 64-bit ), powershell.exe ( same 2 versions ) and bash.exe ( 32-bit ).

When calling cmd.exe or bash.exe with Win+R the 32-bit version is used.

The entries in the console branch are the default values.
When a shortcut is created there are empty values used for colors and other properties. The shortcut colors and fonts following the `hkcu\Console` branch.

When anything is changed on a running shortcut cmd.exe session the current state of colors, fonts, window size are frozen inside the lnk file and any changes in the `hkcu\Console` branch are not longer used from this specific shortcut.

Changes made to cmd.exe or bash.exe which are called from Win+R or batch file are stored
in a separate registry branch like this:

```
[HKEY_CURRENT_USER\Console\%SystemRoot%_system32_cmd.exe]
"FontFamily"=dword:00000036
"FontWeight"=dword:00000190
"FaceName"="Lucida Console"
"ScreenColors"=dword:00000017
```

So changing the initial value of cmd/bash.exe can be done by changing values at `hkcu\Console`.

Changes to Win+R / batch file cmd.exe can be made by changing the values of  the separate branch as described above.
Both changes can be made directly with regedit or copying a branch from a reg-file.

For every cmd.exe, powershell.exe (32, 64) and bash.exe a separate branch is created. So it is (more or less) easy to provide different fonts/colors.

## Changing lnk files directly

For changes inside the lnk files I hadn't found anything helpful on the web in the meantime.

On my computer a lnk file to cmd.exe has a size of 1,274 bytes.
After changing something (font, colors) on a cmd.exe shortcut I got 1,608 bytes.

Maybe with a little bit of reverse engineering I can change the lnk file directly.

## The actual way around

- create a shortcut (but don't change anything in the properties)
- create a reg-file or download one.
- save the actual properties with the command REG
- `REG export hkcu\Console org_colors.reg`
- store the new_colors.reg in the registry with
- `REG import hkcu\Console new_colors.reg`
- open the shortcut and change something like font size
- restore the original colors
- `REG import hkcu\Console org_colors.reg`
- done.

