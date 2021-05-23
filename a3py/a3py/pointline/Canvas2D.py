import drawSvg as draw
from apy.asigpy.maths.Vec3 import *

class Canvas2D(draw.Drawing):
    def __init__(self, width=640, height=480, origin=(0,0), idPrefix='d', displayInline=True, **svgArgs):
        super(Canvas2D, self).__init__(width, height, origin=origin, idPrefix=idPrefix, displayInline=displayInline, **svgArgs);

    @property
    def boundL(self):
        return Vec3(1,0,0);
    @property
    def boundT(self):
        return Vec3(0,1,0);
    @property
    def boundR(self):
        return Vec3(-np.true_divide(1.0,self.width), 0, 1.0);
    @property
    def boundB(self):
        return Vec3(0, -np.true_divide(1.0,self.height), 1.0);

    def drawLineEq(self, l, **kwargs):
        pL=self.boundL.cross(l);
        pR=self.boundR.cross(l);
        pT=self.boundT.cross(l);
        pB=self.boundB.cross(l);

        renderPoints = [];
        if(pL.y>=0 and pL.y<=self.height):
            renderPoints.append(pL);
        if(pR.y>=0 and pR.y<=self.height):
            if(len(renderPoints)==0 or np.linalg.norm(pR._ndarray-renderPoints[0]._ndarray)):
                renderPoints.append(pR);
        if(len(renderPoints)<2):
            if(pT.x>=0 and pT.x<=self.width):
                if(len(renderPoints)==0 or np.linalg.norm(pT._ndarray-renderPoints[0]._ndarray)):
                    renderPoints.append(pT);
        if(len(renderPoints)<2):
            if(pB.x>=0 and pB.x<=self.width):
                if(len(renderPoints)==0 or np.linalg.norm(pB._ndarray-renderPoints[0]._ndarray)):
                    renderPoints.append(pB);
        if(len(renderPoints)>1):
            self.drawLine(renderPoints[0], renderPoints[1], **kwargs);

    def drawLine(self, start, end, stroke='black', **kwargs):
        A = Vec3(start);
        B = Vec3(end);
        self.append(draw.Lines(A.x, A.y, B.x, B.y, stroke=stroke, **kwargs));

    def drawPoint(self, location, color='black', label=None, radius = 15, fontSize=None):
        self.append(draw.Circle(location[0], location[1], radius, fill=color, stroke='black'));
        if(label is not None):
            if(fontSize is None):
                fontSize = radius;
            self.append(draw.Text(label, fontSize=fontSize, x=location[0], y=location[1], center=True, fill='black'));  # Text with font size 8

    def drawCircle(self, center, radius, stroke='black', fill='none', **kwargs):
        self.append(draw.Circle(center.x, center.y, radius, stroke=stroke, fill=fill, **kwargs));



