/**
 * Set data structure.
 */
function Set() {
	this.values = [];
	this.numberOfValues = 0;
}

Set.prototype.add = function(value) {
	if (!~this.values.indexOf(value)) {
		this.values.push(value);
		this.numberOfValues++;
	}
};
Set.prototype.remove = function(value) {
	var index = this.values.indexOf(value);
	if (~index) {
		this.values.splice(index, 1);
		this.numberOfValues--;
	}
};
Set.prototype.contains = function(value) {
	return this.values.indexOf(value) !== -1;
};

Set.prototype.union = function(set) {
	var newSet = new Set();
	set.values.forEach(function(value) {
		newSet.add(value);
	});
	this.values.forEach(function(value) {
		newSet.add(value);
	});
	return newSet;
};
Set.prototype.intersect = function(set) {
	var newSet = new Set();
	this.values.forEach(function(value) {
		if (set.contains(value)) {
			newSet.add(value);
		}
	});
	return newSet;
};
Set.prototype.difference = function(set) {
	var newSet = new Set();
	this.values.forEach(function(value) {
		if (!set.contains(value)) {
			newSet.add(value);
		}
	});
	return newSet;
};
Set.prototype.isSubset = function(set) {
	return set.values.every(function(value) {
		return this.contains(value);
	}, this);
};

Set.prototype.empty = function(){
	this.values = [];
	this.numberOfValues = 0;
};
Set.prototype.print = function() {
	console.log(this.values.join(' '));
};

/**
 * Map Data structure.
 */
function HashTable(size) {
	this.values = {};
	this.numberOfValues = 0;
	this.size = size;
}


HashTable.prototype.add = function(key, value) {
	var hash = this.calculateHash(key);
	if (!this.values.hasOwnProperty(hash)) {
		this.values[hash] = {};
	}
	if (!this.values[hash].hasOwnProperty(key)) {
		this.numberOfValues++;
	}
	this.values[hash][key] = value;
};
HashTable.prototype.remove = function(key) {
	var hash = this.calculateHash(key);
	if (this.values.hasOwnProperty(hash)
			&& this.values[hash].hasOwnProperty(key)) {
		delete this.values[hash][key];
		this.numberOfValues--;
	}
};
HashTable.prototype.calculateHash = function(key) {
	return key.toString().length % this.size;
};
HashTable.prototype.search = function(key) {
	var hash = this.calculateHash(key);
	if (this.values.hasOwnProperty(hash)
			&& this.values[hash].hasOwnProperty(key)) {
		return this.values[hash][key];
	} else {
		return null;
	}
};
HashTable.prototype.length = function() {
	return this.numberOfValues;
};
HashTable.prototype.print = function() {
	var string = '';
	for ( var value in this.values) {
		for ( var key in this.values[value]) {
			string += this.values[value][key] + ' ';
		}
	}
	console.log(string.trim());
};
