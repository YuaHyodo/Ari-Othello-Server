const black = "black";
const white = "white";
const empty = "green";
const black_stone = "X";
const white_stone = "O";
const empty_square = "-";
var index = 0;
var game_sfen = [];
var sfen = "---------------------------OX------XO---------------------------B1"

function change_color(id, color){
document.getElementById(id).style.backgroundColor = color;
return;
}

function add_sfen(add){
game_sfen.push(add);
return;
}

function SfenToHTML(){
if (sfen.indexOf("B") == -1){var color = white;}
else {var color = black;}
change_color("rank", color);
var c = 0;

while (c < 64){
var id = `sq${c}`;
var sq = sfen.substr(c, 1);
if (sq == black_stone){change_color(id, black);}
if (sq == white_stone){change_color(id, white);}
if (sq == empty_square){change_color(id, empty);}
c = c + 1;
}
return;
}

function SfenToStones(){
var black_stones_num = 0;
var white_stones_num = 0;

var c = 0;
while (c < 64){
var sq = sfen.substr(c, 1);
if (sq == black_stone){black_stones_num += 1;}
if (sq == white_stone){white_stones_num += 1;}
c = c + 1;}

var mes = `black_stones:${black_stones_num} white_stones:${white_stones_num} `;
document.getElementById("black_stone_num_show").innerHTML = `Black: ${black_stones_num}`;
document.getElementById("white_stone_num_show").innerHTML = `White: ${white_stones_num}`;
document.getElementById("black_stone_num_show").style.color = white;
document.getElementById("white_stone_num_show").style.color = black;
return;
}

function Plus_index(){
if (index == game_sfen.length - 1){
	return;}
index = index + 1;
sfen = game_sfen[index];
SfenToStones();
SfenToHTML();
return;
}


function Minus_index(){
if (index == 0){
	return;}
index = index - 1;
sfen = game_sfen[index];
SfenToStones();
SfenToHTML();
return;
}

function SetIndex(i){
index = Number(i);
sfen = game_sfen[index];
SfenToStones();
SfenToHTML();
return;
}