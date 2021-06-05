int fatorial(int n){
    if(n == 0){
        return 1;
    }

    return n*fatorial(n-1);
}


int main() {
int c;
c = fatorial(5);
println(c);
}
