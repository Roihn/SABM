# SABM

This is the offical codebase for paper:
**[Smart Agent-Based Modeling: On the Use of Large Language Models in Computer Simulations](https://arxiv.org/abs/2311.06330)**. 

*Zengqing, Wu, Run Peng, Xu Han, Shuyuan Zheng, Yixin Zhang, Chuan Xiao.* 2023. 

> [!NOTE] 
> This codebase is lively under construction!

## Setup

### Environment

We recommend using anaconda to build a virtual environment to test our codes.

```bash
git clone https://github.com/Roihn/SABM.git
cd sabm
conda create -n sabm python=3.10
conda activate sabm
pip install -r requirements.txt
```

### OpenAI API

Please make sure you have the valid openai api key for GPT4. Otherwise, you may need to apply for one before you test our codes. 

Two options are prepared for you to easily apply your api key to our codebase. You can choose either one of them, or both.

1. Setup environment variable

    Run the following command in your terminal.
    
    ```bash
    export OPENAI_API_KEY=<your-api-key>
    ```
    You may need to run it everytime you open a new terminal before you test our codes.

2. Local API storage
    
    This is a one-step setup. You only need to paste your api key in the `apikey.token` file. Then, you can test our codes without any extra setup.

    ***Please do not commit your api key to github, or share it with anyone online.**

## Case Study

> [!WARNING]
> Estimated GPT cost for each case study has been attached aside the titles. Please make sure you have enough allowance and have properly raised the usage limit before you test the code.

### Emergency Evacuation ![Static Badge](https://img.shields.io/badge/GPT-%2440%2Frun-green)


To reproduce the results in the paper, please run the following command.

```bash
python main_emergency_evacuation.py --task <task_id>
```

The `<task_id>` can be one of the following options: [1, 2, 3, 4]. Each task id corresponds to a specific case study in the paper.

Additionally, if you would like to specify a seed, the number of humans, and add obstacles in the environment, you may want to run the following command.

```bash
python main_emergency_evacuation.py --task <task_id> --seed <seed> --num_humans <num_humans> --need_obstacle
```


### Plea Bargaining ![Static Badge](https://img.shields.io/badge/GPT-%2410%2Frun-green)

To reproduce the results in the paper, please run the following command.

```bash
python main_plea_bargain.py
```

We provide a GUI to set the parameters of the run.

```bash
python main_plea_bargain.py --gui
```

If you choose to use command instead of the GUI to set the parameters for simulation, you may want to run the following command.

The `<persona>` can be "persona" or "nopersona", indicating whether or not the persona is used in the performance of plea bargaining.

The `<no_fewshot>` option indicates not to provide a few-shot context to the agent in the plea bargain.

The `<task>` can be one of the following options: [1, 2, 3]. Each task id corresponds to a specific case study in the paper.

```bash
python main_plea_bargain.py --model_version "gpt-4-0314" --tcu_test --persona "nopersona" --no_fewshot --output_max_tokens 100 --num_agents 1 --task 1
```

### Firm Pricing Competition ![Static Badge](https://img.shields.io/badge/GPT-%24300%2Frun-red)


To reproduce the results in the paper, please run the following command.

```bash
python main_firm_pricing_competition.py
```

We provide a GUI to set the parameters of the run.

```bash
python main_firm_pricing_competition.py --gui
```

If you choose to use command instead of the GUI to set the parameters for simulation, you may want to run the following command.
The `<persona_firm>` parameter accepts one of the following options: [0, 1, 2]. Here, 0 indicates no persona, 1 represents an active persona, and 2 denotes an aggressive persona.

```bash
python main_firm_pricing_competition.py --model_version "gpt-4-0314" --rounds 1000 --output_max_tokens 100 --breakpoint_rounds 20 --persona_firm1 1 --persona_firm2 1 --set_initial_price --cost 2 2 --parameter_a 14 --parameter_d 0.00333333333333 --parameter_beta 0.00666666666666 --initial_price 2 2 --load_data_location "Record-231112-1955-gpt-4-0314" --strategy --has_conversation
```


## Citation

If you find our work useful, please give us credit by citing:

```bibtex
@misc{wu2023smart,
      title={Smart Agent-Based Modeling: On the Use of Large Language Models in Computer Simulations}, 
      author={Zengqing Wu and Run Peng and Xu Han and Shuyuan Zheng and Yixin Zhang and Chuan Xiao},
      year={2023},
      eprint={2311.06330},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
}
```
