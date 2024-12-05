if &cp | set nocp | endif
let s:cpo_save=&cpo
set cpo&vim
cmap <D-g> <D-g>
imap <D-g> <D-g>
cmap <D-f> <D-f>
imap <D-f> <D-f>
cmap <D-a> <D-a>
imap <D-a> <D-a>
cnoremap <D-v> +
cnoremap <D-c> 
cmap <D-z> <D-z>
imap <D-z> <D-z>
cmap <S-D-s> <D-s>
imap <S-D-s> <D-s>
cmap <D-s> <D-s>
imap <D-s> <D-s>
cmap <D-w> <D-w>
imap <D-w> <D-w>
cmap <D-o> <D-o>
imap <D-o> <D-o>
cmap <D-n> <D-n>
imap <D-n> <D-n>
xmap gx <Plug>NetrwBrowseXVis
nmap gx <Plug>NetrwBrowseX
nnoremap <silent> <Plug>(vimshell_create) :VimShellCreate
nnoremap <silent> <Plug>(vimshell_switch) :VimShell
xnoremap <silent> <Plug>NetrwBrowseXVis :call netrw#BrowseXVis()
nnoremap <silent> <Plug>NetrwBrowseX :call netrw#BrowseX(netrw#GX(),netrw#CheckIfRemote(netrw#GX()))
omap <D-g> <D-g>
vmap <D-g> <D-g>
nnoremap <D-g> n
omap <D-f> <D-f>
vmap <D-f> <D-f>
nnoremap <D-f> /
omap <D-a> <D-a>
vmap <D-a> <D-a>
nnoremap <silent> <D-a> :if &slm != ""|exe ":norm gggHG"| else|exe ":norm ggVG"|endif
omap <D-z> <D-z>
vmap <D-z> <D-z>gv
nnoremap <D-z> u
omap <S-D-s> <D-s>
vmap <S-D-s> <D-s>gv
nnoremap <S-D-s> :browse confirm saveas
omap <D-s> <D-s>
vmap <D-s> <D-s>gv
nnoremap <silent> <D-s> :if expand("%") == ""|browse confirm w| else|confirm w|endif
omap <D-w> <D-w>
vmap <D-w> <D-w>gv
nnoremap <silent> <D-w> :if winheight(2) < 0 | confirm enew | else | confirm close | endif
omap <D-o> <D-o>
vmap <D-o> <D-o>gv
nnoremap <D-o> :browse confirm e
omap <D-n> <D-n>
vmap <D-n> <D-n>gv
nnoremap <D-n> :confirm enew
vmap <BS> "-d
vnoremap <D-x> "+x
vnoremap <D-c> "+y
nnoremap <D-v> "+gP
let &cpo=s:cpo_save
unlet s:cpo_save
set background=dark
set fileencodings=ucs-bom,utf-8,default,latin1
set runtimepath=~/Documents/.vim,~/Documents/.vim/plugged/vimtex,/private/var/containers/Bundle/Application/154EF669-1683-4804-9303-BE13382923D0/a-Shell.app/vim/vimfiles,/private/var/containers/Bundle/Application/154EF669-1683-4804-9303-BE13382923D0/a-Shell.app/vim,/private/var/containers/Bundle/Application/154EF669-1683-4804-9303-BE13382923D0/a-Shell.app/vim/vimfiles/after,~/Documents/.vim/plugged/vimtex/after,~/Documents/.vim/after
set showcmd
set suffixes=.bak,~,.o,.h,.info,.swp,.obj,.sty,.cls,.log,.aux,.bbl,.out,.blg,.brf,.cb,.dvi,.fdb_latexmk,.fls,.idx,.ilg,.ind,.inx,.pdf,.synctex.gz,.toc
set wildmenu
set wildmode=list:longest
" vim: set ft=vim :
