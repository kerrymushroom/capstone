from chat2agent import evaluate 

def execute_check(code,context,agent,log_name=None):
	result = agent.execute(code,context,log_name)
	if result.status is False:
		return False
	return True

def form_check(code):
	if "plt.show()" not in code:
		return False
	return True

def validity_check(self, code, context, agent, log_name=None):
	results = []
	result = execute_check(code,context,agent,log_name)
	results.append(result)
    if result.answer:
        result = self.surface_form_check(code)
        results.append(result)
    return results	
