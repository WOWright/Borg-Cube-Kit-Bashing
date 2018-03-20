//Pipe elbow
module bend(angle, pipe_run){
    //pipe_run = 3;
    rad = .5;
    $fn = 20;
    rotate([0,90,angle])
    union(){
        cylinder(r=rad, h = pipe_run);
        
        translate([0,rad,pipe_run+rad])
            rotate([-90, 0, 0])
                cylinder(r=rad, h = pipe_run);
        
        translate([0,0,pipe_run]) rotate([0,0,-90])
        hull(){
            cylinder(r=rad, h = .1);
            rotate([0,-90,0])
                translate([rad, 0, rad])
                    cylinder(r=rad, h = .1);
        }
    }
    
}
//Pipe length
module pipe(x, y, length, angle, ht){
    translate([x, y, ht])
    rotate([-90, 0, -angle])
    cylinder(r=.5, h = length, $fn = 20);
}

module full_grate(x, y, thick){
//Create Grate (hardcoded for use on struct_2)
    t = .2;
    w = (.5*y-6*t)/5;
    union(){
        translate([.25*y, 1.75*y, 2*thick])
            cube([.5*y, .2, .2]);
        
        translate([.25*y, 1.25*y, 2*thick])
            cube([.5*y, .2, .2]);
        
        for (i=[0:1:5]){
            translate([.25*y+i*(t+w), 1.25*y, 2*thick])
                grate_bar(.5*y, .2);
        }
    }
}

module grate_bar(L, thick){
    translate([0, L, 0])
        rotate([90,0,0])
            linear_extrude(height = L) 
                polygon(points = [[0,0],[thick,0],[.5*thick,.87*thick]]);
}

//Diamond-ish shape. Use sparingly
module struct_1(x, y, thick){
    difference(){
    hull(){
        cube([x, y, thick]);
        translate([x*.85,y*.85,0]) cube([x, y, thick]);
    };
    translate([x, y, thick/2])
        difference(){
            cylinder(r=.5*min(x,y),h = thick);
            cylinder(r=.35*min(x,y), h = thick);
        }
    }
}


//Set of cubes; varies well with different X and Y. Main portion
module struct_2(x, y, thick){
    union(){
        cube([x, y, thick]);
        translate([x, 0, 0]) 
            cube([.33*x, 1.66*y, thick*1.5]);
        translate([1.33*x, 0, 0]) 
            cube([x, x, thick*.75]);
        translate([0, y, 0]) 
            cube([y, y, 2*thick]);
        
        translate([y, 1.5*y, 0]) 
            cube([1.25*(x-y), .5*y, .67*thick]);
        
        //Add bend and top room
        if (x/4 > .25) {
            translate([1.33*x, .5 ,.75*thick]) 
                bend(0,x-1);
            translate([1.33*x+.25*x, .5*x, .75*thick]) 
                cube([.25*x, .25*x, thick/3]);
        }
        
        //Add straight pipe and full grate
        if (y>1){
        translate([0, y/2, thick]) 
            rotate([90, 0, 90])  
                cylinder(r=.5, h = x, $fn = 20);
        }
        if (rands(0,1,1)[0]>.5)
            full_grate(x, y, thick);
    }
}


//X and Y should be 'close' in size
module struct_3(x, y, thick){
        cube([x,y,thick]);
        translate([2*y, 2*y, 0]) cube([x,y,thick]);
        translate([.75*x, .25*y, 0]) 
            rotate([0,0,45]) 
                cube([2*sqrt(2)*y,.5*y,thick]);
}

//Miter to fit panels together
module edges(x, y, thick){

//    difference(){
//        union(){
//            translate([0, side/sqrt(2), -side/sqrt(2)]) 
//                rotate([45,0,0])
//                    cube([x, side, side]);
//            
//            translate([0, y-side/sqrt(2), -side/sqrt(2)]) 
//                rotate([45,0,0])
//                    cube([x, side, side]);
//            
//            translate([0, 0, 0]) 
//                rotate([0,45,0])
//                    cube([side, y, side]);
//            
//            translate([x-2*side/sqrt(2), 0, 0]) 
//                rotate([0,45,0])
//                    cube([side, y, side]);
//        }
//        cube([x,y,thick*2]);
//    }

    pyramidPts = [[0,0,thick], //0
    [0,2*thick,thick], //1
    [thick,thick,0], //2
    [x,0,thick], //3
    [x,2*thick,thick], //4 
    [x-thick,thick,0]]; //5
    
//    pyramidFaces = [[0, 1, 4, 3], //top
//    [0, 2, 1], //left
//    [0, 2, 5, 3], //front
//    [5, 3, 4], //right
//    [2, 5, 4, 1]]; //back
    
    pyramidFaces = [
    [0, 3, 4, 1], //top/bottom
    [0, 1, 2], //left
    [0, 2, 5, 3], //front
    [4, 3, 5], //right
    [1, 4, 5, 2] //back
    ];
    
    union(){
    polyhedron(points = pyramidPts, faces = pyramidFaces);
    translate([0, y-2*thick, 0]) polyhedron(points = pyramidPts, faces = pyramidFaces);
    translate([2*thick,0,0]) rotate([0,0,90]) polyhedron(points = pyramidPts, faces = pyramidFaces);
    translate([x,0,0]) rotate([0,0,90]) polyhedron(points = pyramidPts, faces = pyramidFaces);
    }
}
