int f1(int n){
    int i;
    i = 0;
    while(i < n){
        println(i);
        i = i+1;
    }
}

int f2(int x){
    if(x > 5){
        return true;
    } else{
        return false;

    }
}

int main() {
    int x;
    bool y;
    x = 6;
    f1(x);
    y = f2(x);
    println(y);
}
