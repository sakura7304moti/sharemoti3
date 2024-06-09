import { ref } from 'vue';
import { NameListApi } from 'src/api/main/NameListApi';
import { useSsbuListModel } from './SsbuListModels';

export function useSsbuRankModels() {
  const {
    //スマブラのキャラ名
    ssbuNames,
    getSsbuNames,
    //スマブラの切り抜き
    records,
    search,
  } = getRecords();

  const rankRecords = ref({
    ultraC: [] as RankState[],
    ulturaC: [] as RankState[],
    memory: [] as RankState[],
    yaki: [] as RankState[],
  } as Rank);

  const rankBase = ref([] as RankBase[]);

  const movieGroup = ['ウルトラC', 'ウルツラC', '思い出', '焼き直し'];

  const setRank = function () {
    //タグ別にセット
    rankBase.value.splice(0);
    records.value.forEach((it) => {
      movieGroup.forEach((tag) => {
        if (it.fileName.includes(tag)) {
          const pushName = ssbuNames.value.find(
            (s) => s.name == it.charName
          ) ?? {
            name: '',
            url: '',
            smallUrl: '',
          };
          rankBase.value.push({
            tag: tag,
            ssbuName: pushName,
          });
        }
      });
    });

    //集計
    rankRecords.value.ultraC.splice(0);
    rankRecords.value.ulturaC.splice(0);
    rankRecords.value.memory.splice(0);
    rankRecords.value.yaki.splice(0);

    const ulCBase = rankBase.value.filter((it) => it.tag == 'ウルトラC');
    const charBase = new Set(ulCBase.map((it) => it.ssbuName.name));
    charBase.forEach((charName) => {
      rankRecords.value.ultraC.push();
    });
  };

  return {
    //スマブラのキャラ名
    ssbuNames,
    getSsbuNames,
    //スマブラの切り抜き
    records,
    search,
  };
}

function getRecords() {
  /*スマブラのキャラ名 */
  const nameApi = new NameListApi();
  const ssbuNames = ref([] as SsbuName[]);
  const getSsbuNames = async function () {
    await nameApi.ssbu_names().then((response) => {
      if (response) {
        ssbuNames.value.splice(0);
        response.records.forEach((it) => ssbuNames.value.push(it));
      }
    });
  };

  /*切り抜きの一覧 */
  const { records, search } = useSsbuListModel();

  return {
    //スマブラのキャラ名
    ssbuNames,
    getSsbuNames,
    //スマブラの切り抜き
    records,
    search,
  };
}
interface SsbuName {
  name: string;
  url: string;
  smallUrl: string;
}
interface SsbuClip {
  id: number;
  charName: string;
  fileName: string;
  displayFileName: string;
  date: string;
  displayDate: string;
  year: string;
}
interface RankState {
  rank: number;
  clipCount: number;
  ssbuName: SsbuName;
}
interface Rank {
  ultraC: RankState[];
  ulturaC: RankState[];
  memory: RankState[];
  yaki: RankState[];
}
interface RankBase {
  tag: string;
  ssbuName: SsbuName;
}
