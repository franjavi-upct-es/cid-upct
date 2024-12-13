" TABLE OF CONTENTS:

" 1. Generic settings
" 2. File settings
" 3. UI
" 4. Maps and functions

"-----------------------------------------
" 1. GENERIC SETTINGS
"-----------------------------------------

set nocompatible " disable vi compatibility mode
set history=1000 " increase history size

"-----------------------------------------
" 2. FILE SETTINGS
"-----------------------------------------

" Stop creating backup files, please use Git for backups

set nobackup
set nowritebackup
set noswapfile
set backspace=indent,eol,start

" Modify indenting settings

set autoindent " autoindent always ON.
set expandtab " expand tabs
set shiftwidth=2 " spaces for autoindenting
set softtabstop=2 " remove a full pseudo-TAB when i press <BS>
set clipboard=unnamedplus
set wrap

" Modify some other settings about files

set encoding=utf-8 " always use unicode
set hidden
set ignorecase
set mouse=a                   " Habilitar uso del ratón en todas las ventanas
set ttymouse=sgr              " Mejor compatibilidad del ratón en terminales modernos
set scrolloff=8 " Keep at least 8 lines below cursor
set foldmethod=manual " To avoid performance issues, I never fold anything so...

"-----------------------------------------
" 3. UI
"-----------------------------------------

set fillchars+=vert:\ " Remove unpleasant pipes from vertical splits

" Sauce on this: http://stackoverflow.com/a/9001540

set wildmenu " enable visual wildmenu
set number " show line numbers
set showmatch " higlight matching parentheses and brackets
set nohlsearch
set lazyredraw
set ttyfast
set hidden
syntax on

call plug#begin()
" Plugins generales
Plug 'preservim/nerdtree'                  " Navegador de archivos
Plug 'junegunn/fzf', { 'do': './install --all' } " Búsqueda rápida
Plug 'junegunn/fzf.vim'
Plug 'vim-airline/vim-airline'            " Barra de estado
Plug 'ervandew/supertab'                  " Autocompletado con Tab
Plug 'preservim/tagbar'                   " Vista de clases y funciones

Plug 'sirver/ultisnips'
  let g:UltiSnipsExpandTrigger = '<tab>'
  let g:UltiSnipsJumpForwardTrigger = '<tab>'
  let g:UltiSnipsJumpBackwardTrigger = '<s-tab>'

Plug 'lervag/vimtex'
  let g:tex_flabor='latex'
  let g:vimtex_quickfix_mode=0

Plug 'KeitaNakamura/tex-conceal.vim'

" RMarkdown y Quarto
Plug 'vim-pandoc/vim-pandoc'              " Pandoc para Markdown/RMarkdown
Plug 'vim-pandoc/vim-pandoc-syntax'       " Resaltado de sintaxis Markdown
Plug 'iamcco/markdown-preview.nvim', { 'do': 'cd app && yarn install' }

" Python
Plug 'davidhalter/jedi-vim'               " Autocompletado Python
Plug 'psf/black', { 'branch': 'main' }    " Formateador Black

Plug 'jiangmiao/auto-pairs'
Plug 'matze/vim-move'
call plug#end()


" Configuración para Zathura como visor PDF
let g:vimtex_view_method = 'zathura'
let g:vimtex_compiler_method = 'latexmk'
let g:vimtex_compiler_latexmk = {
      \ 'build_dir' : 'build',
      \ 'options' : [
      \   '-pdf',
      \   '-interaction=nonstopmode',
      \   '-synctex=1',
      \ ],
      \}

" Configuración de markdown-preview
let g:mkdp_auto_start = 1                " Activar vista previa automáticamente

" Configuración de NERDTree
map <C-n> :NERDTreeToggle<CR>            " Atajo para abrir/cerrar NERDTree


" Configuración de Tagbar
nmap <F8> :TagbarToggle<CR>              " Atajo para abrir/cerrar Tagbar

" ===============================
" Configuración estética
" ===============================
set background=dark                      " Tema oscuro

" ===============================
" Atajos personalizados
" ===============================
" Guardar rápido
nnoremap <C-s> :w<CR>
" Salir rápido
nnoremap <C-q> :q<CR>
" Atajo para compilar y abrir el PDF con Zathura
nnoremap <C-CR> :VimtexCompile<CR>:VimtexView<CR>
vnoremap <C-c> "+y"
