@0xda57732f03a1d319;

struct Picture {    
    png @0 :Data;
    timestamp @1 :UInt64;
}

struct Resolution {
    width @0 :Int32;
    height @1 :Int32;
}

interface FeedbackCamera {
    get @0 () -> (picture :Picture);
    calibrate @1 () -> (); 
    detectCanvas @2 () -> (); 
    updateLightmap @3 () -> (); 
    updateColorBalance @4 () -> ();
    imageResolution @5 () -> (size :Resolution);
}
