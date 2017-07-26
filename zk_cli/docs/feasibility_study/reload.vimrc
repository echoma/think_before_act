set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
"set rtp+=~/.vim/bundle/Vundle.vim
"call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
"Plugin 'VundleVim/Vundle.vim'
"Plugin 'Valloric/YouCompleteMe'
"call vundle#end()

"Plugin 'auto_autoread.vim'


filetype plugin indent on
colorscheme darkblue
set nobackup
set nu
set ts=4
set sw=4
set backspace=indent,eol,start
set fdm=syntax
set foldnestmax=2
set foldcolumn=3
set guifont=文泉驿等宽微米黑\ 9
set autoread


imap <S-PageDown> <Esc>:bn<CR>a
nmap <S-PageDown> :bn<CR>
imap <S-PageUp> <Esc>:bp<CR>a
nmap <S-PageUp> :bp<CR>

imap <C-p> <Esc>:bp<CR>a
nmap <C-p> :bp<CR>
imap <C-n> <Esc>:bn<CR>a
nmap <C-n> :bn<CR>

"imap <C-g> <Esc>:YcmCompleter GoTo<CR>a
"nmap <C-g> :YcmCompleter GoTo<CR>

"imap <C-d> <Esc>:YcmCompleter GoToImplementationElseDeclaration<CR>a
"nmap <C-d> :YcmCompleter GoToImplementationElseDeclaration<CR>

augroup checktime
    au!
    if !has("gui_running")
        "silent! necessary otherwise throws errors when using command
        "line window.
        autocmd BufEnter        * silent! checktime
        autocmd CursorHold      * silent! checktime
        autocmd CursorHoldI     * silent! checktime
        "these two _may_ slow things down. Remove if they do.
        autocmd CursorMoved     * silent! checktime
        autocmd CursorMovedI    * silent! checktime
    endif
augroup END


