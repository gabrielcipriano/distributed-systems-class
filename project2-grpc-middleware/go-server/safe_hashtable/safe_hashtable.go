package safe_hashtable

import (
	"sync"
)

// SafeHashtable the set of Items
type SafeHashtable struct {
	items map[string]int32
	lock  sync.RWMutex
}

// Put item with int32 v and string k into the hashtable
func (ht *SafeHashtable) Put(k string, v int32) {
	ht.lock.Lock()
	defer ht.lock.Unlock()
	ht.items[k] = v
}

func (ht *SafeHashtable) Create() {
	ht.items = make(map[string]int32)
}

// Get item with string k from the hashtable
func (ht *SafeHashtable) Get(k string) int32 {
	ht.lock.RLock()
	defer ht.lock.RUnlock()
	return ht.items[k]
}
