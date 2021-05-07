from typing import List


class WorkflowResult:
    def __init__(self, model_result: dict, model_name: str = None):
        self.result = model_result
        self.model_name = model_name

    def set_model_name(self):
        """
        Checks self.model_name and attempts to set it if not already specified. Raises error if multiple models are available.
        """
        if self.model_name:
            self._check_is_valid_model_name()
        elif len(self.available_model_names) > 1:
            raise RuntimeError(
                f"Multiple models available, you must set self.model_name to one of {self.available_model_names}"
            )
        else:
            self.model_name = self.available_model_names[0]

    def _check_is_valid_model_name(self) -> None:
        if self.model_name not in self.available_model_names:
            raise KeyError(
                f"{self.model_name} is not an available model name. Options: {self.available_model_names}"
            )

    @property
    def predictions(self) -> List[dict]:
        self.set_model_name()
        preds = self.document_results[self.model_name]
        if isinstance(preds, dict):
            return preds["pre_review"]
        else:
            return preds

    @property
    def post_review_predictions(self) -> List[dict]:
        self.set_model_name()
        try:
            return self.document_results[self.model_name]["final"]
        except KeyError:
            raise Exception(f"Submission {self.submission_id} has not completed Review")

    @property
    def etl_url(self) -> str:
        return self.result["etl_output"]

    @property
    def document_results(self) -> dict:
        return self.result["results"]["document"]["results"]

    @property
    def available_model_names(self) -> list:
        return list(self.document_results.keys())

    @property
    def submission_id(self) -> str:
        return self.result["submission_id"]
    
    @property
    def errors(self) -> list:
        return self.result["errors"]

    @property
    def review_id(self) -> int:
        return self.result["review_id"]

    @property
    def reviewer_id(self) -> int:
        return self.result["reviewer_id"]
    
    @property
    def review_notes(self) -> int:
        return self.result["review_notes"]

    @property
    def review_rejected(self) -> int:
        return self.result["review_rejected"]
    
    @property
    def admin_review(self) -> bool:
        return self.result["admin_review"]