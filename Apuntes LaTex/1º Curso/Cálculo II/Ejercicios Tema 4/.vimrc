set nu
syntax on

set mouse=a

set softtabstop=4
set shiftwidth=4
set autoindent
set expandtab
set smartindent

autocmd FileType python map <buffer> <space> :w<CR>:exec '!python3' shellescape(@%, 1)<CR>
autocmd FileType python imap <buffer> <space> <esc>:w<CR>:exec '!python3' shellescape(@%, 1)<CR>
