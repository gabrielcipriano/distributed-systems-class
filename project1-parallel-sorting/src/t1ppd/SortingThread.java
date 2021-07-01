package t1ppd;

import java.util.List;

public class SortingThread extends Thread {
	private List<Double> list;
	private String strategy;
	
	public SortingThread(List<Double> list, String strategy) {
		if(!(strategy.equals("merge") || strategy.equals("sort"))) {
			throw new Error("Strategy param must be 'sort' or 'merge'");
		}
		
		this.list = list;
		this.strategy = strategy;
	}
	
	public SortingThread(List<Double> list) {
		this.list = list;
		this.strategy = "sort";
	}
	
	@Override
	public void run() {
		if (strategy.equals("merge")) {
			Utils.merge(list);
		}
		if (strategy.equals("sort") ) {
			list.sort(null);
		}
	}
}
