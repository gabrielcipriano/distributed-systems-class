package t1ppd;

import java.util.ArrayList;
import java.util.List;

public class Utils {
	
	//	Inspirado no mergesort, ordena uma lista que possui as duas metades ordenadas
	public static void merge(List<Double> list) {
		int n = list.size();
		int middle = n/2;
		int index = 0;
		
		
		ArrayList<Double> helper = new ArrayList<Double>(list);
		
		int i = index;
		int j = middle;
		
		while (i < middle && j < n) {
			if (helper.get(i) < helper.get(j)) {
				list.set(index, helper.get(i));
				i++;
			}else {
				list.set(index, helper.get(j));
				j++;
			}
			index++;
		}
		
		// se a metade inicial não foi toda consumida, faz o append.
        while (i < middle) {
            list.set(index, helper.get(i));
            i++;
            index++;
        }	
		
	}
	
	
	public static boolean isPowerOfTwo(int x){
		// explanation: http://graphics.stanford.edu/~seander/bithacks.html#DetermineIfPowerOf2
	    return (x != 0) && ((x & (x - 1)) == 0);
	}
}
