from __future__ import annotations
from typing import Optional
from .exceptions import BkwException
from .rest_adapter import RestAdapter
from .data_models import Case
import logging

class BkwApi:
    def __init__(self, hostname: str = 'api.bk.watch/api', ver: str = '2022-08-01', username: str = "", password: str = "", ssl_verify: bool = True, logger: logging.Logger = None):
        self._logger = logger or logging.getLogger(__name__)
        self._rest_adapter = RestAdapter(hostname, ver, username, password, ssl_verify, logger)

    def run_docket(self, district: str, extendedCaseNumber: str, fromDate: Optional[str] = '', toDate: Optional[str] = '', fromItem: Optional[int] = None, toItem: Optional[int] = None, pacerAccount: Optional[str] = '', cache: bool = True) -> Case:
        ep_params = {
            'district': district,
            'extendedCaseNumber': extendedCaseNumber,
            'dateType': 'filed',
        }
        if cache: ep_params['cache'] = 'true'
        if not cache: ep_params['cache'] = 'false'
        if fromDate: ep_params['fromDate'] = fromDate
        if toDate: ep_params['toDate'] = toDate
        if fromItem: ep_params['fromItem'] = fromItem
        if toItem: ep_params['toItem'] = toItem
        if pacerAccount: ep_params['pacerAccount'] = pacerAccount
        result = self._rest_adapter.get(operation="RunDocket", ep_params=ep_params)
        if (not result.bkw_response) or (not 'case' in result.bkw_response):
            self._logger.warning(msg="No results found from the request.")
            raise BkwException("No case found.")
        return Case.parse_obj(result.bkw_response['case'])
        
    def run_claims_register(self, district: str, extendedCaseNumber: str, fromDate: Optional[str] = '', toDate: Optional[str] = '', fromClaim: Optional[int] = None, toClaim: Optional[int] = None, pacerAccount: Optional[str] = '', cache: Optional[bool] = True) -> Case:
        ep_params = {
            'district': district,
            'extendedCaseNumber': extendedCaseNumber,
        }
        if cache: ep_params['cache'] = 'true'
        if not cache: ep_params['cache'] = 'false'
        if fromDate: ep_params['fromDate'] = fromDate
        if toDate: ep_params['toDate'] = toDate
        if fromClaim: ep_params['fromClaim'] = fromClaim
        if toClaim: ep_params['toClaim'] = toClaim
        if pacerAccount: ep_params['pacerAccount'] = pacerAccount
        result = self._rest_adapter.get(operation="RunClaimsRegister", ep_params=ep_params)
        if (not result.bkw_response) or (not 'case' in result.bkw_response):
            self._logger.warning(msg="No case found in the response.")
            raise BkwException("No case found.")
        return Case.parse_obj(result.bkw_response['case'])
