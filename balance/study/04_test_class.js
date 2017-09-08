class Parent {
    constructor() {
        this.name = Parent.randName();
    }

    static randName() {
        return 'P'+Math.random();
    }
}
Parent.foo = 1;

class Child extends Parent {
    static randName() {
        return 'C'+Math.random();
    }
}

let c = new Child();

console.log(c.name);

console.log(Parent.foo);