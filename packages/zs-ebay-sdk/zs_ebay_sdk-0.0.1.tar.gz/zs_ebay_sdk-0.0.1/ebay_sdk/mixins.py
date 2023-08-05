__all__ = [
    "EbayNextUrlActionMixin",
]


class EbayNextUrlActionMixin:
    def run_action(self, **kwargs):
        results_stack = []

        # set first step params
        step_params = self.prepare_params(**kwargs)

        while True:
            # execute action
            objects = self.make_request(**step_params)
            step_results = objects.get("results", None)

            if isinstance(step_results, list):
                results_stack += step_results
            else:
                results_stack.append(step_results)

            # break if condition is not met
            if self.multistep_action_condition(
                step_results=step_results,
                step_params=step_params,
            ):
                # set next step action params
                step_params = self.get_next_step_action_params(
                    step_results=step_results,
                    step_params=step_params,
                )
            else:
                break

        # process results
        results = self.process_results(results_stack)
        # save results of all steps
        return {"results": results}

    def prepare_params(self, **params) -> dict:
        return params

    def process_results(self, results_stack: list):
        return results_stack

    def multistep_action_condition(self, step_results: dict, **kwargs) -> bool:
        if isinstance(step_results, dict):
            return step_results.get("next", None)
        return False

    def get_next_step_action_params(
        self, step_results: dict = None, step_params: dict = None
    ) -> dict:
        step_params["next_url"] = step_results.get("next", None)
        return step_params
