# !/bin/env sh

function build_ctags()
{

    ctags -R --c++-kinds=+px --fields=+iaS --extra=+q -L filelist
}
