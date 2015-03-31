function insertEmpty(count) {
    var every = 10000
    var bulk = db.c.initializeUnorderedBulkOp();
    var t = new Date()
    for (var i=0; i<=count; i++) {
        if (i>0 && i%every==0) {
            bulk.execute();
            bulk = db.c.initializeUnorderedBulkOp();
            tt = new Date()
            print(i, Math.floor(every / (tt-t) * 1000))
            t = tt
        }
        bulk.insert({})
    }
}

function insert(count) {
     every = 1000
     var t = new Date()
     for (var i=0; i<count; ) {
         var bulk = db.c.initializeUnorderedBulkOp();
         for (var j=0; j<every; j++, i++)
             bulk.insert({a:"a", b:"this is a long string that keeps on going", i:i, j:j, date:t})
         bulk.execute();
     }
}
