" Plugins - Plug"

function! DoRemote(arg)
  UpdateRemotePlugins
endfunction

call plug#begin('~/.vim/plugged')
Plug 'flazz/vim-colorschemes' "A good many colorschemes"
Plug 'Shougo/deoplete.nvim', { 'do': function('DoRemote') } "Autocomplete"
Plug 'vim-airline/vim-airline' | Plug 'vim-airline/vim-airline-themes' "status bar along with themes"
Plug 'scrooloose/nerdtree' "Filebrowser"
Plug 'jistr/vim-nerdtree-tabs' "NerdTree for tabs"
Plug 'tpope/vim-commentary' "Fast Commenting"
Plug 'tpope/vim-fugitive' "Git support"
Plug 'ctrlpvim/ctrlp.vim' "Fuzzy file browser"
Plug 'airblade/vim-gitgutter' "Git symbols on the side"
Plug 'ntpeters/vim-better-whitespace'
Plug 'jiangmiao/auto-pairs' "Let's get them brackets together"
Plug 'majutsushi/tagbar' "Tags baby"
Plug 'scrooloose/syntastic'
Plug 'Yggdroot/indentLine'
Plug 'sheerun/vim-polyglot'
call plug#end()

"Plugin - Settings"

let g:deoplete#enable_at_startup=1

let g:ctrlp_match_window = 'bottom,order:ttb'
let g:ctrlp_switch_buffer = 0
let g:ctrlp_working_path_mode = 0
let g:airline_powerline_fonts = 1

set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*

let g:syntastic_always_populate_loc_list = 1
let g:syntastic_auto_loc_list = 0
let g:syntastic_check_on_open = 0
let g:syntastic_check_on_wq = 0

" Keybindings"
let mapleader=","   " leader is comma
let g:mapleader = ","   " leader is comma
let g:polyglot_disabled = ['python']

"Open NERDTree
map <C-n> :NERDTreeToggle<cr>

" Long lines are now breaks
map j gj
map k gk

nmap <F8> :TagbarToggle<CR>
nmap <F5> :SyntasticCheck<CR>
nmap <F6> :Errors<CR>

"Save""
nmap <leader>w :w!<CR>

"Clear Hightlighting"
map <silent> <leader><cr> :noh<cr> :StripWhitespace<cr>

" Close the current buffer
map <leader>bd :tabclose<cr>gT

" Close all the buffers
map <leader>ba :bufdo bd<cr>

map <leader>l :bnext<cr>
map <leader>h :bprevious<cr>

" Useful mappings for managing tabs
map <leader>tn :tabnew<cr>
map <leader>to :tabonly<cr>
map <leader>tc :tabclose<cr>
map <leader>tm :tabmove <cr>
map <leader>t<leader> :tabnext <cr>

" Pressing ,ss will toggle and untoggle spell checking
map <leader>ss :setlocal spell!<cr>

" Shortcuts using <leader>
map <leader>sn ]s
map <leader>sp [s
map <leader>sa zg
map <leader>s? z=

" Commands

" Sudo saves the file
command W w !sudo tee % > /dev/null

" Visual Config"
set encoding=utf-8 "UTF Encoding
set t_Co=256 "256 Color Support"
colorscheme badwolf  "Badass Colorscheme
set bg=dark

" Editor Config"
syntax enable "Syntax highlighting
set tabstop=2 "Spaces per tab that are shown
set softtabstop=2 "Spaces per tab that are written
set expandtab "Tabs are now space
set shiftwidth=2 "Align spaces and tab"
set lazyredraw "Fucking stop drawing shit
set clipboard+=unnamedplus "Clipboard compatibility"
set colorcolumn=79 "Limit line length to make for easier reading.

" UI Config
set number " Show line numbers
set so=10 "10 line buffer when scrolling

