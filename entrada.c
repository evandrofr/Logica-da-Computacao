{
    bool loop;
    int x;
    x = 0;
    loop = true;
    while(loop){
        x = x + 1;
        println(x);
        if(x > 10){
            loop = false;
        }
    }

}
