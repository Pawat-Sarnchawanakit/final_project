# Project Evaluation Proposal
## Introduction

This proposal outlines the necessary steps and actions to be taken for evaluating a project in the administrative process involved in doing a senior project. The evaluation step is added to the existing process and is conducted after the project report submission and before the final approval by the advisor. The evaluation step involves a group of faculties who assess the project report and provide feedback and recommendations.
##  Evaluation Actions
1. **Assign Evaluators**: When a project report is submitted by a group, the system assigns a group of faculties as evaluators for that project. The number of evaluators can be determined based on the size and complexity of the project. The system should ensure that evaluators are assigned fairly, considering their workload and expertise.

2. **Notify Evaluators**: The system sends notification messages to the assigned evaluators, informing them about the project they need to evaluate. The notification includes details such as the project title, group members, and the due date for evaluation.

3. **Access Project Report**: The evaluators should have access to the submitted project report in order to review and evaluate it. The system should provide a secure and convenient way for evaluators to download or access the project report.

4. **Evaluate Project Report**: The evaluators review and evaluate the project report based on predetermined evaluation criteria. This step involves assessing various aspects such as project objectives, methodology, results, analysis, and overall quality of the report. Each evaluator provides individual feedback and assigns a score or rating to the project report.

5. **Compile Evaluations**: Once all evaluators have completed their assessment, the system compiles the individual evaluations into a consolidated evaluation report. This report should include the feedback, scores, and any additional comments provided by the evaluators.

6. **Notify Lead and Advisor**: The system sends notifications to the lead student and the advisor, informing them that the project evaluation has been completed. The notification should include a summary of the evaluation results and any recommendations or suggestions provided by the evaluators.

7. **Review Evaluation Results**: The lead student and the advisor review the evaluation results and feedback. They can access the consolidated evaluation report through the system. This step allows them to understand the strengths and weaknesses of the project as identified by the evaluators.

8. **Revise Project (if needed)**: Based on the evaluation feedback, the lead student and the group members may need to make revisions or improvements to the project. They should have the opportunity to refine their project based on the evaluation results before proceeding to the final approval step.

9. **Submit Revised Project (if applicable)**: If revisions are made to the project based on the evaluation feedback, the group submits the revised project report to the advisor for further evaluation. This step ensures that the project meets the required standards and addresses the identified issues.

10. **Final Approval**: After the evaluation and potential revision steps, the advisor reviews the final project report and makes a final decision regarding its approval. If the project meets the required criteria and addresses the evaluation feedback adequately, the advisor approves the project.

# Implementation Details

The following code snippets outline the implementation of the evaluation actions described above. Please note that these snippets are simplified examples and may require adaptation to fit.
1. **Assign Evaluators** and **Notify Evaluators**:
```py
select_random_evalutors().send_to_evaluation_queue_and_alert(project)
```
2. **Access report**
```py
if is_evaluator(project):
    project.get_report().open()
```
3. **Compile Evaluations**
```py
compiled_evaluation = evaluation.compile()
```
4. **Notify Lead and Advisor**
```py
project.getLead().notify(Type.Evaluation, compiled_evaluation)
project.getAdvisor().notify(Type.Evaluation, compiled_evaluation)
```
5. **Review Evaluation Results**
```py
project.getEvaluation().show();
```
6. **Revise Project (if needed):**
```py
project.update([NEW DETAILS HERE])
```
7. **Submit Revised Project (if applicable):**
```py
project.submit();
```
8. **Final Approval**
```py
def check_final_evaluation(project):
    for evaluator in project.getEvaluators():
        if not evaluator.approved:
            return False
    return True
if check_final_evaluation(project):
    project.status = ProjectStatus.Approved;
```
# Conclusion

The proposed project evaluation process adds a crucial step to the administrative process of senior projects. By incorporating the outlined actions, the evaluation step ensures that projects are thoroughly reviewed, evaluated, and provided with feedback and recommendations. This iterative process allows students to improve their projects based on evaluation results and ultimately enhances the quality of the final project outcomes.