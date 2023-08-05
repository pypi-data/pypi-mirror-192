"""
support commandline parameter insert to running
# instances
python api_example.py --ray_args.local_mode --env_args.difficulty=6  --algo_args.num_sgd_iter=6
----------------- rules -----------------
1 ray/rllib config: --ray_args.local_mode
2 environments: --env_args.difficulty=6
3 algorithms: --algo_args.num_sgd_iter=6
order insensitive
-----------------------------------------

-------------------------------available env-map pairs-------------------------------------
- smac: (https://github.com/oxwhirl/smac/blob/master/smac/env/starcraft2/maps/smac_maps.py)
- mpe: (https://github.com/Replicable-MARL/MARLlib/blob/main/envs/base_env/mpe.py)
- mamujoco: (https://github.com/Replicable-MARL/MARLlib/blob/main/envs/base_env/mamujoco.py)
- football: (https://github.com/Replicable-MARL/MARLlib/blob/main/envs/base_env/football.py)
- magent: (https://github.com/Replicable-MARL/MARLlib/blob/main/envs/base_env/magent.py)
- lbf: use (https://github.com/Replicable-MARL/MARLlib/blob/main/envs/base_env/config/lbf.yaml) to generate the map.
Details can be found https://github.com/semitable/lb-foraging#usage
- rware: use (https://github.com/Replicable-MARL/MARLlib/blob/main/envs/base_env/config/rware.yaml) to generate the map.
Details can be found https://github.com/semitable/robotic-warehouse#naming-scheme
- pommerman: OneVsOne-v0, PommeFFACompetition-v0, PommeTeamCompetition-v0
- metadrive: Bottleneck, ParkingLot, Intersection, Roundabout, Tollgate
- hanabi: Hanabi-Very-Small, Hanabi-Full, Hanabi-Full-Minimal, Hanabi-Small
-------------------------------------------------------------------------------------------


-------------------------------------available algorithms-------------------------------------
- iql pg a2c ddpg trpo ppo
- maa2c coma maddpg matrpo mappo hatrpo happo
- vdn qmix facmac vda2c vdppo
----------------------------------------------------------------------------------------------
"""

from marllib import marl

# prepare the environment
env = marl.make_env(environment_name="mpe", map_name="simple_spread")
# can add extra env params. remember to check env configuration before use
# env = marl.make_env(environment_name='smac', map_name='3m', difficulty="6", reward_scale_rate=15)

# initialize algorithm and load hyperparameters
mappo = marl.algos.mappo(hyperparam_source='common')
# can add extra algorithm params. remember to check algo hyperparams before use
# mappo = marl.algos.MAPPO(hyperparam_source='common', use_gae=True,  batch_episode=10, kl_coeff=0.2, num_sgd_iter=3)

# start learning + extra experiment settings if needed. remember to check ray.yaml before use
mappo.fit(env, stop={'episode_reward_mean': 2000, 'timesteps_total': 10000000}, local_mode=True, num_gpus=0,
          num_workers=2, share_policy='all', checkpoint_freq=5)
