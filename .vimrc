au BufRead,BufNewFile *.kv set syntax=kivy

let @k='matsysskill.py'
nnoremap <F10> :update %<CR>:!kivy <C-R>k<CR>
