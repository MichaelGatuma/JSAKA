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
Set.prototype.length = function() {
	return this.numberOfValues;
};
Set.prototype.print = function() {
	console.log(this.values.join(' '));
};
