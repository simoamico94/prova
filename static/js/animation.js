/*==============CENTRAL FIBER ANIMATION============*/
var c,
	ctx,
	w,
	h,
	cx,
	cy,
	branches,
	startHue,
	tick;

function rand( min, max ) {
	return Math.random() * ( max - min ) + min;
}

function randInt( min, max ) {
	return Math.floor( min + Math.random() * ( max - min + 1 ) );
};

function Branch( hue, x, y, angle, vel ) {
	var move = 15;
	this.x = x + rand( -move, move );
	this.y = y + rand( -move, move );
	this.points = [];
	this.angle = angle != undefined ? angle : rand( 0, Math.PI * 1 );
	this.vel = vel != undefined ? vel : rand( -4, 4 );
	this.spread = 0;
	this.tick = 0;
	this.hue = hue != undefined ? hue : 200;
	this.life = 1;
	this.decay = 0.0015;
	this.dead = false;

	this.points.push({
		x: this.x,
		y: this.y
	});
}

Branch.prototype.step = function( i ) {
	this.life -= this.decay;
	if( this.life <= 0 ) {
		this.dead = true;
	}

	if( !this.dead ) {
		var lastPoint = this.points[ this.points.length - 1 ];
		this.points.push({
			x: lastPoint.x + Math.cos( this.angle ) * this.vel,
			y: lastPoint.y + Math.sin( this.angle ) * this.vel
		});
		this.angle += rand( -this.spread, this.spread );
		this.vel *= 0.985;
		this.spread = this.vel * 0.04;
		this.tick++;
		this.hue += 0.3;
	} else {
		branches.splice( i, 1 );
	}
};

Branch.prototype.draw = function() {
	if( !this.points.length || this.dead ) {
		return false;
	}

	var length = this.points.length,
		i = length - 1,
		point = this.points[ i ],
		lastPoint = this.points[ i - randInt( 5, 100 ) ];
		//jitter = 8;
	if( lastPoint ) {
		var jitter = 2 + this.life * 6;
		ctx.beginPath();
		ctx.moveTo( lastPoint.x, lastPoint.y );
		ctx.lineTo( point.x + rand( -jitter, jitter ), point.y + rand( -jitter, jitter ) );
		ctx.lineWidth = 1;
		var alpha = this.life * 0.075;
		ctx.strokeStyle = 'hsla(' + ( this.hue + rand( -10, 10 ) ) + ', 70%, 40%, ' + alpha + ')';
		ctx.stroke();
	}
}

function init() {
	c = document.getElementById( 'c' );
	ctx = c.getContext( '2d' );
	startHue = 220;
	branches = [];
	reset();
	loop();
}

function reset() {
	w = window.innerWidth;
	h = window.innerHeight;
	cx = w / 2;
	cy = h / 2;
	branches.length = 0;
	c.width = w;
	c.height = h;
	tick = 0;


	for( var i = 0; i < 500; i++ ) {
		branches.push( new Branch( startHue, cx, cy) );
	}
}

function step() {
	var i = branches.length;
	while( i-- ) { branches[ i ].step( i ) }
	tick++;
}

function draw() {
	var i = branches.length;
	if( tick < 450 ) {
		ctx.save();
		ctx.globalCompositeOperation = 'lighter';
		ctx.globalAlpha = 0.002;
		ctx.translate( cx, cy );
		var scale = 1 + tick * 0.00025 ;
		ctx.scale( scale, scale );
		ctx.translate( -cx, -cy );
		ctx.drawImage( c, rand( -150, 150 ), rand( -150, 150 ) );
		ctx.restore();
	}

	ctx.globalCompositeOperation = 'lighter';
		while( i-- ) { branches[ i ].draw() }
}

function loop() {
	requestAnimationFrame( loop );
	step();
	draw();
	step();
	draw();
}

window.addEventListener( 'resize', reset );
window.addEventListener( 'click', function() {
	startHue += 60;
	reset();
});

init();

/*=================BACKGROUND ANIMATION================*/
var scene = document.getElementById('scene');
var parallax = new Parallax(scene);

for (var i = 1; i < 6; i++) {
  twinkleLoop(i);
};

function twinkleLoop(i) {
  var duration = ((Math.random() * 5) + 3)
 duration = duration - ((495 - speed)/100)
  twinkle(i, duration)
  setTimeout(function() {
    twinkleLoop(i)
  }, duration * 1000);
}

function twinkle(id, duration) {
  var top = (Math.floor(Math.random() * 85) + 0) + '%';
  var left = (Math.floor(Math.random() * 85) + 0) + '%';

  $('#speck' + id).remove();
  $('#specks').append("<div class='speck' id='speck" + id + "'></div>")
  $('#speck' + id).css({
    'top': top,
    'left': left,
    'animation-duration': duration + 's',
    'animation-timing-function': 'cubic-bezier(0.250, 0.250, 0.750, 0.750)',
    'animation-name': 'twinkle',
  })
}

 var speed = 400;
//SLIDER
$(document).ready(function(){
 $("#slider").on("change", function() {
       $('.speck').remove();
  for (var i = 1; i < 4; i++) {

    speed = 201 - this.value;
    $('#range').text('1000px / '+(speed/10)+'s')
    speed = speed * (i / 1.25)
    $('#img-' + i).css({
      'animation-duration': speed + 's',
      'animation-name': 'float'
    });
  }
});
})

/*======== HIDE SHOW MENU ============*/

function showDiv(n)
{
document.getElementById("div"+n).style.display = 'block'
return false;
}

function hideDiv(n)
{
for (x=1; x<=10; x++)
{
document.getElementById("div"+x).style.display = 'none'
}
document.getElementById(n).style.display = 'block'
return false;
}

function toggleDiv(id)
{

	for (x=1; x<=3; x++)
	{
		document.getElementById("div"+x).style.display = 'none';
	}
	var hexArray = ['#f9a55b','#fcfe6c','#68ff6e', '#6ac0fb', '#fa53f7', '#f60000']
	var randomColor = hexArray[Math.floor(Math.random() * hexArray.length)];
	document.getElementById(id).style.display = 'block';
	document.getElementById(id).style.background = randomColor;
}

function hideAll()
{
	for (x=1; x<=3; x++)
	{
		document.getElementById("div"+x).style.display = 'none';
	}
}
