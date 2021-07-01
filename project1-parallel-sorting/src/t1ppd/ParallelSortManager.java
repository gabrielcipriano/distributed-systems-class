package t1ppd;

import java.util.ArrayList;
import java.util.List;

public class ParallelSortManager {
	private ArrayList<SortingThread> threads;
	
	
	
	// @strategy: 
	//		'sort'  : ordena completamente
	//		'merge' : ordena uma lista que possui as duas metades ordenadas
	public ParallelSortManager(ArrayList<Double> list, int k, String strategy) {
		if(!Utils.isPowerOfTwo(k)) {
			throw new Error("K must be power of two");
		}
		
		this.threads = new ArrayList<>();
		
		int n = list.size();
		
		List<Double> slice;
		
		for(int i=0; i<k; i++) {
			slice = list.subList(i*n/k,(i+1)*n/k);
			this.threads.add(new SortingThread(slice, strategy));
		}
		
	}
	
	public void startAll() {
		for (SortingThread thread : threads) {
			thread.start();
		}
	}
	
	public void joinAll() throws InterruptedException {
		for (SortingThread thread : threads) {
			thread.join();
		}
	}

}
