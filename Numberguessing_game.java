import java.util.Random;
import java.util.Scanner;

class Random_Number{
    int num;
    void Generate(){
    Random r=new Random();
    num=r.nextInt(100)+1;
}
}

class Guessing_number extends Random_Number{
    Scanner sc=new Scanner(System.in);
    int guess=0;
    void play(){
    while(guess!=num){
        System.out.println("Enter your guess: ");
        int g=sc.nextInt();

        if(g>num){
            System.out.println("Too High");
        }
        else if(g<num){
            System.out.println("Too Low");
        }
        else{
            System.out.println("Correct! You Guessed The Number");
            break;
        }
    }
}
}
public class Numberguessing_game {
    public static void main(String args[]){
    Guessing_number game=new Guessing_number();
    game.Generate();
    game.play();
}
}
