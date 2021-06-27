import matlab.engine

eng = matlab.engine.start_matlab()
content = eng.load('/data/f16_AerodynamicData.mat')