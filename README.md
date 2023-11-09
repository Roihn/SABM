# SABM

This is the offical codebase for paper:
**[Smart Agent-Based Modeling: On the Use of Large Language Models in Computer Simulations]()**. 

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

Two options are prepared for you to easily enter your api key with our codebase. You can choose either one of them, or both.

1. Setup envirionment variable

    Run the following command in your terminal.
    
    ```bash
    export OPENAI_API_KEY=<your-api-key>
    ```
    You may need to run it everytime you open a new terminal before you test our codes.

2. Local API storage
    
    This is a one-step setup. You only need to paste your api key in the `apikey.token` file. Then, you can test our codes without any extra setup.

    > [!WARNING]  
    > Please do not commit your api key to github, or share it with anyone online.

## Case Study


### Emergency Evacuation

To reproduce the results in the paper, please run the following command.

```bash
python main_emergency_evacuation.py --task <task_id>
```

The `<task_id>` can be one of the following options: [1, 2, 3, 4]. Each task id corresponds to a specific case study in the paper.

Additionally, if you would like to specify a seed, the number of humans, and add obstacles in the environment, you may want to run the following command.

```bash
python main_emergency_evacuation.py --task <task_id> --seed <seed> --num_humans <num_humans> --need_obstacle
```

> [!WARNING]  
> This part of experiments consumes around $40 per trial because of the openai api usage. Please make sure you have enough allowance and have properly raise the usage limit before you test the code.



### Plea Bargaining

Coming soon...

### Firm Pricing Competition

Coming soon...

## Citation

If you find our work useful, please give us credit by citing:

```bibtex
@article{wu2023smart,
  title={Smart Agent-Based Modeling: On the Use of Large Language Models in Computer Simulations},
  author={Wu, Zengqing and Peng, Run and Han, Xu and Zheng, Shuyuan and Zhang, Yixin and Xiao, Chuan},
  year={2023}
}
```
