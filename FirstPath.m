sim=remApi('remoteApi'); % using the prototype file (remoteApiProto.m)
sim.simxFinish(-1); % just in case, close all opened connections
clientID=sim.simxStart('127.0.0.1',19999,true,true,5000,5);
sim.simxSynchronous(clientID, true);
if (clientID>-1)
    disp("Hooray")
    [returncode, ball]= sim.simxGetObjectHandle(clientID,'/target',sim.simx_opmode_blocking);
    [returnCode,position]=sim.simxGetObjectPosition(clientID,ball,-1,sim.simx_opmode_streaming);

    for i=1:50
        [returnCode,position]=sim.simxGetObjectPosition(clientID,ball,-1,sim.simx_opmode_buffer);
        disp(position)
    end
   
    sim.simxFinish(-1);
end
sim.delete();

% sim=remApi('remoteApi'); % using the prototype file (remoteApiProto.m)
% sim.simxFinish(-1); % just in case, close all opened connections
% clientID=sim.simxStart('127.0.0.1',19999,true,true,5000,5);
% if (clientID>-1)
%         disp('Connected to remote API server');
%         %code here
%         %Handle
%         [returnCode,left_Motor]=sim.simxGetObjectHandle(clientID,'./leftMotor',sim.simx_opmode_blocking);
%         [returnCode,front_sensor]=sim.simxGetObjectHandle(clientID,'./ultrasonicSensor[4]',sim.simx_opmode_blocking);
%         [returnCode,camera]=sim.simxGetObjectHandle(clientID,'./Vision_sensor',sim.simx_opmode_blocking);
% 
% 
%         [returnCode,resolution,image]=sim.simxGetVisionSensorImage2(clientID,camera,0,sim.simx_opmode_streaming);
% 
%         [returnCode,detectionState,detectedPoint,~,~]=sim.simxReadProximitySensor(clientID,front_sensor,sim.simx_opmode_streaming);
% 
%         [returnCode]=sim.simxSetJointTargetVelocity(clientID,left_Motor,2,sim.simx_opmode_blocking);
%         for i=1:50
%             [returnCode,detectionState,detectedPoint,~,~]=sim.simxReadProximitySensor(clientID,front_sensor,sim.simx_opmode_buffer);
%             [returnCode,resolution,image]=sim.simxGetVisionSensorImage2(clientID,camera,0,sim.simx_opmode_streaming);
%             imshow(image);
%             disp(norm(detectedPoint));
%             pause(0.1)
%         end
% 
%         [returnCode]=sim.simxSetJointTargetVelocity(clientID,left_Motor,0,sim.simx_opmode_blocking);
%         sim.simxFinish(-1);
% end
% sim.delete();