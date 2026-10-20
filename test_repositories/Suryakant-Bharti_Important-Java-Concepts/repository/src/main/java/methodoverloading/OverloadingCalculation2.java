package methodoverloading;

public class OverloadingCalculation2 {
    public void sum(int a, int b) {
        System.out.println("int arg method invoked");
    }
    public void sum(long a, long b) {
        System.out.println("long arg method invoked");
    }

    public static void main(String[] args) {
        OverloadingCalculation2 obj = new OverloadingCalculation2();
        obj.sum(20, 20); // int arg sum() method gets invoked
    }
}