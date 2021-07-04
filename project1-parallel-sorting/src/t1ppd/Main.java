package t1ppd;

import java.text.NumberFormat;
import java.util.ArrayList;
import java.util.Random;


public class Main {

	public static void main(String[] args) throws InterruptedException {
		
		final int n = 50000000;
		final int[] ks = {8, 4, 2, 1};
		final ArrayList<Double> list = generateRandomList(n);
		
		System.out.println("Size: " + NumberFormat.getIntegerInstance().format(n));
		

		long startTime;
		ArrayList<Double> cloneList;
		ParallelSortingThread sortingThread;
		
		for (int k : ks) {
			cloneList = new ArrayList<Double>(list);
			startTime = System.currentTimeMillis();
			
			sortingThread = new ParallelSortingThread(cloneList, k);
			sortingThread.start();
			sortingThread.join();
			
			System.out.printf("k=%d runtime: %d ms\n", k, System.currentTimeMillis()-startTime);
		}
		
	}
	
	
	
	private static ArrayList<Double> generateRandomList(int size){
		Random random = new Random();
		ArrayList<Double> list = new ArrayList<Double>();

		for (int i = 0; i < size; i++) {
			list.add(random.nextDouble());
		}
		
		return list;
	}

}
