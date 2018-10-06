import gym
from gym import spaces
from gym.utils import seeding
import numpy as np
from os import path
import ode
import math
import cv2

class ReacherEnv(gym.Env):
    metadata = {
        'render.modes' : ['human', 'rgb_array'],
        'video.frames_per_second' : 5
    }
    def create_link(self,body,pos):
        body.setPosition(pos)
        M = ode.Mass()
        M.setCylinderTotal(1,1,0.1,1)
        M.translate((0.5,0,0))
        M.setParameters(M.mass,0,M.c[1],M.c[2],M.I[0][0],M.I[1][1],M.I[2][2],M.I[0][1],M.I[0][2],M.I[1][2])
        body.setMass(M)

    def create_ee(self,body,pos,collision):
        body.setPosition(pos)
        M = ode.Mass()
        M.setCylinderTotal(0.000000001, 1,0.000001,0.000001)
        body.setMass(M)
        collision.setBody(body)
    def init_rod_template(self):
        self.rod_template_1 = np.matrix(np.zeros((int(math.ceil(self.resolution)+10),int(math.ceil(self.resolution)+10))))
        self.rod_template_1[5:5+int(math.ceil(self.resolution)),int(math.floor(((math.ceil(self.resolution)+10)/2.0)-(self.resolution*0.15))):int(math.ceil(((math.ceil(self.resolution)+10)/2.0)+(self.resolution*0.15)))]=1
        self.rod_template_1 = self.rod_template_1.T

        self.rod_template_2 = np.matrix(np.zeros((int(math.ceil(self.resolution)+10),int(math.ceil(self.resolution)+10))))
        self.rod_template_2[5:5+int(math.ceil(self.resolution)),int(math.floor(((math.ceil(self.resolution)+10)/2.0)-(self.resolution*0.1))):int(math.ceil(((math.ceil(self.resolution)+10)/2.0)+(self.resolution*0.1)))]=1
        self.rod_template_2 = self.rod_template_2.T

        self.rod_template_3 = np.matrix(np.zeros((int(math.ceil(self.resolution)+10),int(math.ceil(self.resolution)+10))))
        self.rod_template_3[5:5+int(math.ceil(self.resolution)),int(math.floor(((math.ceil(self.resolution)+10)/2.0)-(self.resolution*0.05))):int(math.ceil(((math.ceil(self.resolution)+10)/2.0)+(self.resolution*0.05)))]=1
        self.rod_template_3 = self.rod_template_3.T

    def __init__(self):
        self.dt=.005
        self.viewer = None
        self.viewerSize = 500
        self.spaceSize = 6.4
        self.resolution = self.viewerSize/self.spaceSize
        self.init_rod_template()
        self.seed()
        self.world = ode.World()
        #self.world.setGravity((0,-9.81,0))
        self.world.setGravity((0,0,0))
        self.body1 = ode.Body(self.world)
        self.body2 = ode.Body(self.world)
        self.body3 = ode.Body(self.world)
        self.body4 = ode.Body(self.world)
        self.create_link(self.body1,(0.5,0,0))
        self.create_link(self.body2,(1.5,0,0))
        self.create_link(self.body3,(2.5,0,0))
        self.space = ode.Space()
        self.body4_col = ode.GeomSphere(self.space,radius=0.1)
        self.create_ee(self.body4,(3,0,0),self.body4_col)

        # Connect body1 with the static environment
        self.j1 = ode.HingeJoint(self.world)
        self.j1.attach(self.body1, ode.environment)
        self.j1.setAnchor( (0,0,0) )
        self.j1.setAxis( (0,0,1) )
        self.j1.setFeedback(1)

        # Connect body2 with body1
        self.j2 = ode.HingeJoint(self.world)
        self.j2.attach(self.body1, self.body2)
        self.j2.setAnchor( (1,0,0) )
        self.j2.setAxis( (0,0,-1) )
        self.j2.setFeedback(1)

        #connect body3 with body2
        self.j3 = ode.HingeJoint(self.world)
        self.j3.attach(self.body2, self.body3)
        self.j3.setAnchor( (2,0,0) )
        self.j3.setAxis( (0,0,-1) )
        self.j3.setFeedback(1)

        #connect end effector
        self.j4 = ode.FixedJoint(self.world)
        self.j4.attach(self.body3,self.body4)
        self.j4.setFixed()

        self.controlMode = "POS"
        self.targetPos = self.rand_target()
        self.targetTime = 0
        self.P_gains = np.array([1000,1000,1000])
        self.D_gains = np.array([70,50,20])

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def saturation(self,joint_angle,joint_velocity,target_angle,limitedVel,kp,kd):
        lamb = kp/kd
        x_tild = joint_angle-target_angle
        if(x_tild==0):
            return 0
        sat = limitedVel/(lamb*np.abs(x_tild))
        scale = 1
        if(sat<1):
            unclipped = kp*x_tild
            clipped = kd * limitedVel * np.sign(x_tild)
            scale= 1 * clipped/unclipped
        torque = (-kd * (joint_velocity + np.clip(sat/scale,0,1)*scale*lamb*x_tild))
        return torque

    def pd_control(self,jas,jvs,target_jas):
        pos_gains = np.diag(self.P_gains)
        damp_gains = np.diag(self.D_gains) #np.matrix([[100,0,0],[0,60,0],[0,0,20]])
        return np.array(pos_gains*(np.matrix(angle_normalize(target_jas-jas))).T).flatten()-np.array((damp_gains*np.matrix(jvs).T).T).flatten()

    def pd_vel_control(self,jas,jvs):
        pos_gains = np.diag(self.P_gains)
        damp_gains = np.diag(self.D_gains) #np.matrix([[100,0,0],[0,60,0],[0,0,20]])
        return np.array(pos_gains*np.matrix(jas).T).flatten()-np.array((damp_gains*np.matrix(jvs).T).T).flatten()

    def rand_target(self):
        pos = (np.random.rand(2,1)-0.5)*4
        self.targetGeom = ode.GeomSphere(self.space, radius=0.1)
        self.targetGeom.setPosition((pos[0],pos[1],0))
        return pos

    def near_callback(self,args, geom1, geom2):
        """Callback function for the collide() method.

        This function checks if the given geoms do collide and
        creates contact joints if they do.
        """
        # Check if the objects do collide
        contacts = ode.collide(geom1, geom2)
        if(len(contacts)>0):
            self.targetTime+=self.dt
        else:
            self.targetTime=0

    def step(self,(jas,jvs,target_ja,torques)):
        if(self.controlMode=="POS"):
            jointAngles = np.array([self.j1.getAngle(),self.j2.getAngle(),self.j3.getAngle()])
            jointVelocities = np.array([self.j1.getAngleRate(), self.j2.getAngleRate(), self.j3.getAngleRate()])
            output_torques = self.pd_control(jointAngles,jointVelocities,target_ja)
            self.j1.addTorque(output_torques[0])
            self.j2.addTorque(output_torques[1])
            self.j3.addTorque(output_torques[2])
        if(self.controlMode=="POS-SLOW"):
            self.j1.addTorque(self.saturation(self.j1.getAngle(),self.j1.getAngleRate(),target_ja[0],0.8,self.P_gains[0],self.D_gains[0]))
            self.j2.addTorque(self.saturation(self.j2.getAngle(),self.j2.getAngleRate(),target_ja[1],0.8,self.P_gains[1],self.D_gains[1]))
            self.j3.addTorque(self.saturation(self.j3.getAngle(),self.j3.getAngleRate(),target_ja[2],0.8,self.P_gains[2],self.D_gains[2]))
        if(self.controlMode=="POS-IMG"):
            torques = self.pd_control(jas,jvs,target_ja)
            self.j1.addTorque(torques[0])
            self.j2.addTorque(torques[1])
            self.j3.addTorque(torques[2])
        if(self.controlMode=="VEL"):
            #self.D_gains = np.array([60,50,40])
            #self.P_gains = np.array([400,400,400])
            torques = self.pd_vel_control(jas,jvs)
            self.j1.addTorque(torques[0])
            self.j2.addTorque(torques[1])
            self.j3.addTorque(torques[2])
        if(self.controlMode=="TORQUE"):
            self.j1.addTorque(torques[0])
            self.j2.addTorque(torques[1])
            self.j3.addTorque(torques[2])
        self.world.step(self.dt)
        self.space.collide(self.world,self.near_callback)
        if(self.targetTime>1.0):
            self.targetPos=self.rand_target()
            self.targetTime=0

    def reset(self):
        high = np.array([np.pi, 1])
        self.state = self.np_random.uniform(low=-high, high=high)
        self.last_u = None
        return self.get_obs()

    def get_obs(self):
        theta, thetadot = self.state
        return np.array([np.cos(theta), np.sin(theta), thetadot])

    def render(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return
        x1,y1,z1 = self.body1.getPosition()
        x2,y2,z2 = self.body2.getPosition()
        x3,y3,z3 = self.body3.getPosition()
        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(self.viewerSize,self.viewerSize)
            self.viewer.set_bounds(-self.spaceSize/2.0,self.spaceSize/2.0,-self.spaceSize/2.0,self.spaceSize/2.0)

            rod1 = rendering.make_capsule(1, .3)
            rod1.set_color(0.4, 0.4, 0.4)
            self.pole_transform1 = rendering.Transform()
            self.pole_transform11 = rendering.Transform()
            rod1.add_attr(self.pole_transform1)
            rod1.add_attr(self.pole_transform11)
            self.viewer.add_geom(rod1)


            rod2 = rendering.make_capsule(1, .2)
            rod2.set_color(0.2, 0.2, 0.2)
            self.pole_transform2 = rendering.Transform()
            self.pole_transform21 = rendering.Transform()
            rod2.add_attr(self.pole_transform2)
            rod2.add_attr(self.pole_transform21)
            self.viewer.add_geom(rod2)

            rod3 = rendering.make_capsule(1, .1)
            rod3.set_color(0,0,0)
            self.pole_transform3 = rendering.Transform()
            self.pole_transform31 = rendering.Transform()
            rod3.add_attr(self.pole_transform3)
            rod3.add_attr(self.pole_transform31)
            self.viewer.add_geom(rod3)

            axle1 = rendering.make_circle(.2)
            axle1.set_color(1,0,0)

            self.axle_transform1 = rendering.Transform()
            axle1.add_attr(self.axle_transform1)
            self.viewer.add_geom(axle1)
            self.axle_transform12 = rendering.Transform()
            axle1.add_attr(self.axle_transform12)
            axle2 = rendering.make_circle(.15)
            axle2.set_color(0,1,0)
            self.axle_transform2 = rendering.Transform()
            axle2.add_attr(self.axle_transform2)
            self.axle_transform22 = rendering.Transform()
            axle2.add_attr(self.axle_transform22)
            self.viewer.add_geom(axle2)
            axle3 = rendering.make_circle(.1)
            axle3.set_color(0,0,1)
            self.axle_transform3 = rendering.Transform()
            axle3.add_attr(self.axle_transform3)
            self.axle_transform32 = rendering.Transform()
            axle3.add_attr(self.axle_transform32)
            self.viewer.add_geom(axle3)
            target = rendering.make_circle(.05)
            target.set_color(0.7,0.7,0.7)
            self.viewer.add_geom(target)
            self.targetTrans = rendering.Transform()
            target.add_attr(self.targetTrans)
            #fname = path.join(path.dirname(__file__), "assets/clockwise.png")
            #self.img = rendering.Image(fname, 1., 1.)
            #self.imgtrans = rendering.Transform()
            #self.img.add_attr(self.imgtrans)
        self.transform_link(self.body1,self.pole_transform11,self.pole_transform1,self.axle_transform12,self.axle_transform1)
        self.transform_link(self.body2,self.pole_transform21,self.pole_transform2,self.axle_transform22,self.axle_transform2)
        self.transform_link(self.body3,self.pole_transform31,self.pole_transform3,self.axle_transform32,self.axle_transform3)
        self.targetTrans.set_translation(self.targetPos[0],self.targetPos[1])
        return self.viewer.render(True)

    def transform_link(self,body, t1, t2, j1, j2):
        x1,y1,z1 = body.getPosition()
        (x,y,z,w) = body.getQuaternion()
        (X,Y,Z) = Quaternion_toEulerianAngle(x,y,z,w)
        t1.set_translation(x1,y1)
        t1.set_rotation(-X)
        t2.set_translation(-0.5,0)
        j1.set_translation(x1,y1)
        j1.set_rotation(-X)
        j2.set_translation(-0.5,0)


def angle_normalize(x):
    return (((x+np.pi) % (2*np.pi)) - np.pi)

def Quaternion_toEulerianAngle(x, y, z, w):
	ysqr = y*y
	t0 = +2.0 * (w * x + y*z)
	t1 = +1.0 - 2.0 * (x*x + ysqr)
	X = (math.atan2(t0, t1))
	t2 = +2.0 * (w*y - z*x)
	t2 =  1 if t2 > 1 else t2
	t2 = -1 if t2 < -1 else t2
	Y = (math.asin(t2))
	t3 = +2.0 * (w * z + x*y)
	t4 = +1.0 - 2.0 * (ysqr + z*z)
	Z = (math.atan2(t3, t4))
	return X, Y, Z
