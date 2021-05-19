{
    string x;
    string y;
    bool a;
    x = readln();
    y = "maca";
    println(x == y);
    println(x + y);
    a = true;
    println(!a || false);
    if(""){
        println(1);
    } else {
        println(2);
    }
    int num;
    int num2;
    int num3;
    num = 2;
    num2 = 1;
    num3 = -1;
    if((!(num > 1)  || (num2 == 0)) && (num3 > 0)){
        println(3);
    } else {
        while(!(1 == 0 || 1 == 2) && (num < 5)) {
            num = num + 1;
            num2 = num2 + 2;
            println("loop");
        }
    }

    println("aviao" + true);
}
