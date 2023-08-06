from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Tuple, Optional

from .base_ssdb import BaseSsdb
from .utils import SsdbResponseUtils


class BaseSsdbSortedSet(BaseSsdb):

    def zsize(self, name: str) -> int:
        pass

    def zset(self, name: str, key: str, score: float):
        pass

    def multi_zset(self, name: str, score_mapping: Dict[str, float]) -> int:
        pass

    def multi_zget(self, name: str, keys: List[str]) -> Dict[str, float]:
        pass

    def zrank(self, name: str, key: str) -> int:
        pass

    def zrrank(self, name: str, key: str) -> int:
        pass

    def zrange(self, name: str, offset: int, size: int) -> List[Tuple[str, float]]:
        pass

    def zrrange(self, name: str, offset: int, size: int) -> List[Tuple[str, float]]:
        pass

    def get_ranking(self, name: str, rank: int) -> Optional[Tuple[int, str]]:
        pass

    def multi_get_ranking(self, name: str, ranks: List[int]) -> Dict[int, str]:
        pass

    def multi_get_ranking2(self, name: str, ranks: List[int]) -> Dict[int, str]:
        pass

    def zdel(self, name: str, key: str):
        pass

    def multi_zdel(self, name: str, keys: List[str]) -> bool:
        pass

    def zclear(self, name: str):
        pass


class SsdbSortedSet(BaseSsdbSortedSet):
    thread_executor = ThreadPoolExecutor(max_workers=8)

    def zsize(self, name: str) -> int:
        result = self.execute_command('zsize', name)
        return result

    def zset(self, name: str, key: str, score: float):
        result = self.execute_command(
            'zset',
            name,
            key,
            score
        )

    def multi_zset(self, name: str, score_mapping: Dict[str, float]) -> int:
        pairs = SsdbResponseUtils.encode_dict_to_pairs(score_mapping)
        result = self.execute_command('multi_zset', name, *pairs)

        return int(result) if result is not None else 0

    def multi_zget(self, name: str, keys: List[str]) -> Dict[str, float]:
        result = self.execute_command('multi_zget', name, *keys)

        return {
            k.decode('utf-8'): float(v)
            for k, v in SsdbResponseUtils.response_to_map(result).items()
        }

    def zrank(self, name: str, key: str) -> int:
        result = self.execute_command('zrank', name, key)
        return int(result) if result is not None else None

    def zrrank(self, name: str, key: str) -> int:
        result = self.execute_command('zrrank', name, key)
        return int(result) if result is not None else None

    def zrange(self, name: str, offset: int, size: int) -> List[Tuple[str, float]]:
        result = self.execute_command('zrange', name, offset, size)
        return [
            (k.decode('utf-8'), float(v))
            for k, v in SsdbResponseUtils.response_to_pair_list(result)
        ]

    def zrrange(self, name: str, offset: int, size: int) -> List[Tuple[str, float]]:
        result = self.execute_command('zrrange', name, offset, size)
        return [
            (k.decode('utf-8'), float(v))
            for k, v in SsdbResponseUtils.response_to_pair_list(result)
        ]

    def get_ranking(self, name: str, rank: int) -> Optional[Tuple[int, str]]:
        if rank > 0:
            start_rank, end_rank = rank, rank
            response = self.execute_command('zrange', name, start_rank, end_rank + 1)
            rank_to_id_map = SsdbResponseUtils.to_rank_to_id_map(response, [rank], start_rank)

            id = rank_to_id_map.get(rank, None)
        else:
            id = None

        return (rank, id) if id is not None else None

    def multi_get_ranking2(self, name: str, ranks: List[int]) -> Dict[int, str]:
        rank_2_ids: Dict[int, str] = {}

        if len(ranks) > 0:
            future_list = [
                SsdbSortedSet.thread_executor.submit(self.get_ranking, name, rank)
                for rank in ranks
            ]
            for future in futures.as_completed(future_list):
                result = future.result()
                if result is not None:
                    rank = int(result[0])
                    id = str(result[1])
                    rank_2_ids[rank] = id

        return rank_2_ids

    def multi_get_ranking(self, name: str, ranks: List[int]) -> Dict[int, str]:
        actual_result_map: Dict[int, str] = {}

        if len(ranks) > 0:
            start_rank, end_rank = max(0, min(ranks)), max(ranks)
            response = self.execute_command('zrange', name, start_rank, end_rank + 1)
            rank_to_id_map = SsdbResponseUtils.to_rank_to_id_map(response, ranks, start_rank)

            for rank in ranks:
                if rank in rank_to_id_map.keys():
                    actual_result_map[rank] = rank_to_id_map[rank]
        return actual_result_map

    def zdel(self, name: str, key: str):
        result = self.execute_command('zdel', name, key)

    def multi_zdel(self, name: str, keys: List[str]) -> bool:
        self.execute_command('multi_zdel', name, *keys)
        return True

    def zclear(self, name: str):
        result = self.execute_command('zclear', name)
