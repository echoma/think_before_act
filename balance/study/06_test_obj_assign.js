let a = {'name':'a', 'sex':'man'};
let b = {'name':'b', 'sex':'women'};
let c = {'name':'c', 'sex':undefined};

let x = Object.assign(a,b,c);

console.log(x);
