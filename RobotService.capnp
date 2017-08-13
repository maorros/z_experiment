@0xfdb51feaa7ad108f;

# Tool center point
struct Point {
    x @0 :Float64;
    y @1 :Float64;
    z @2 :Float64;
}

# Tool orientation
struct Quaternion {
    x @0 :Float64;
    y @1 :Float64;
    z @2 :Float64;
    w @3 :Float64;
}

struct Pose {
    position @0 :Point;
    orientation @1 :Quaternion;
    velocity @2 :Float64 = 0.5; # relative velocity
}

struct Size2D {
    width @0 :Float64;
    height @1 :Float64;
}

struct Status {
    pose @0 :Pose;
    error @1 :Error;  
    slotTool @2 : Int32 = 0;
    slotPaint @3 : Int32 = 0;
    
    enum Error {
        ok @0;
        transformation @1;
        unknown @2;
        missingArgument @3;
	badCommand @4;
	notImplemented @5;
	invalidRobotLocation @6;
	robotMovementFailure @7;
	pathTooLong @8;
        connectionFailed @9;
        connectionLost @10;
        badResponse @11;
        robotPointBufferFull @12;
        startFailure @13;
        stopFailure @14;
        robotErrorState @15;
	robotNotStarted @16;
    }
}

enum MovementMacro {
    homePose @0;
    hidePose @1;
}

interface RobotService {
    movePose @0 (pose :Pose) -> (status :Status);
    movePath @1 (poses :List(Pose)) -> (status :Status);
    stop @2 () -> (status :Status);
    start @3 () -> (status :Status);
    getStatus @4 () -> (status :Status); 
    dipSlotPaint @5 (index :Int32) -> (status :Status);
    fetchTool @6 (index :Int32) -> (status :Status);
    washTool @7 (secs :Int32) -> (status :Status);
    movePoseSafe @8 (pose :Pose) -> (status :Status);
    movePathSafe @9 (poses :List(Pose)) -> (status :Status);
    moveMacro @10 (arg :MovementMacro) -> (status :Status);
    getCanvasSize @11 () -> (size :Size2D);
}
