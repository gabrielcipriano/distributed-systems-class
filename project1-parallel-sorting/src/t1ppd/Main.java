package t1ppd;

import java.util.ArrayList;
import java.util.Random;

public class Main {

	public static void main(String[] args) throws InterruptedException {
		int n = 50000000;
		n = 1000;
		
		int k = 1;
		
		Random random = new Random();
		ArrayList<Double> list = new ArrayList<Double>();

		for (int j = 0; j < n; j++) {
			list.add(random.nextDouble());
		}
		
		//debug
		ArrayList<Double> list2 = new ArrayList<Double>(list);
		
//		System.out.println(list);
		
		ParallelSortManager sortManager;
		long start = System.currentTimeMillis();
		
		// sort step
		sortManager = new ParallelSortManager(list, k, "sort");
		sortManager.startAll();
		sortManager.joinAll();
		
		//	merge step 
		for(int i = k/2; i >= 1; i = i/2) {
			sortManager = new ParallelSortManager(list, i, "merge");
			sortManager.startAll();
			sortManager.joinAll();
		}
//		System.out.println(list);
		System.out.println("M:" + (System.currentTimeMillis()-start));
		list2.sort(null);
		System.out.println(list.equals(list2));

	}

}
