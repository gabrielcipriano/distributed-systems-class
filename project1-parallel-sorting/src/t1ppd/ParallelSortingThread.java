package t1ppd;

import java.util.List;

public class ParallelSortingThread extends Thread {
	private List<Double> list;
	private int k;
	
	public ParallelSortingThread(List<Double> list, int k) {
		
		if(!Utils.isPowerOfTwo(k)) {
			throw new Error("K must be power of two");
		}
		
		this.list = list;
		this.k = k;
	}
	
	@Override
	public void run() {
		if (k == 1) {
			list.sort(null);
			return;
		}
		
		int n = list.size();
		
		ParallelSortingThread left = new ParallelSortingThread(list.subList(0, n/2), k/2);
		ParallelSortingThread right = new ParallelSortingThread(list.subList(n/2, n), k/2);
		
		left.start();
		right.start();
		
		try {
			left.join();
			right.join();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		
		Utils.merge(list);
		
	}
}
