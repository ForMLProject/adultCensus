import sys
import os

class AdultException(Exception):
    def __init__(self, error_message:Exception,error_detail:sys):
        super().__init__(error_message)
        self.error_message = AdultException.get_exception(error_message=error_message,error_detail=error_detail)

    @staticmethod
    def get_exception(error_message:Exception,error_details:sys):
        _,_,exec_tb = error_details.exc_info()
        exception_line_no = exec_tb.tb_frame.f_lineno
        try_block_line_number = exec_tb.tb_lineno
        file_name = exec_tb.tb_frame.f_code.co_filename
        error_message = f"""
        Error occured in script: 
        [ {file_name} ] at 
        try block line number: [{try_block_line_number}] and exception block line number: [{exception_line_no}] 
        error message: [{error_message}]
        """
        return error_message
        
    def __str__(self):
        return self.error_message

    def __repr__(self) -> str:
        return AdultException.__name__.str()