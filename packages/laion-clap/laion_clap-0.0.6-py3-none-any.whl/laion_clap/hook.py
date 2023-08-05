"""
Contrastive Language-Audio Pretraining Model from LAION
--------------------------------------------------------
Paper: https://arxiv.org/abs/2211.06687
Authors (equal contributions): Ke Chen, Yusong Wu, Tianyu Zhang, Yuchen Hui
Support: LAION
"""
import progressbar
import os
import torch
import librosa
from open_clip import create_model
from training.data import get_audio_features
from training.data import int16_to_float32, float32_to_int16
from transformers import RobertaTokenizer
import wget
from open_clip.factory import load_state_dict
try:
  from urllib.request import urlretrieve
except ImportError:
  from urllib import urlretrieve

pbar = None

def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()
    downloaded = block_num * block_size
    print(downloaded, total_size)
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None


class CLAP_Module:
    def __init__(self) -> None:
        device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        precision = 'fp32'
        amodel = 'HTSAT-tiny' # or 'PANN-14'
        tmodel = 'roberta' # the best text encoder in our training
        enable_fusion = True # False if you do not want to use the fusion model
        fusion_type = 'aff_2d'
        model, model_cfg = create_model(
            amodel,
            tmodel,
            precision=precision,
            device=device,
            enable_fusion=enable_fusion,
            fusion_type=fusion_type
        )
        self.model = model
        self.model_cfg = model_cfg
        self.tokenize = RobertaTokenizer.from_pretrained('roberta-base')

    def tokenizer(self, text):
        result = self.tokenize(
            text,
            padding="max_length",
            truncation=True,
            max_length=77,
            return_tensors="pt",
        )
        return {k: v.squeeze(0) for k, v in result.items()}

    def load_ckpt(self, ckpt = None):
        """Load the pretrained checkpoint of CLAP model

        Parameters
        ----------
        ckpt: str
            if ckpt is specified, the model will load this ckpt, otherwise the model will download the ckpt from zenodo.
        """
        if ckpt is not None:
            print(f'Load the specified checkpoint {ckpt} from users.')
        else:
            print(f'Load our best checkpoint in the paper.')
            package_dir = os.path.dirname(os.path.realpath(__file__))
            weight_file_name = 'laion_clap_fullset_fusion.pt'
            ckpt = os.path.join(package_dir, weight_file_name)
            if os.path.exists(ckpt):
                print(f'The checkpoint is already downloaded')
            else:
                print('Downloading laion_clap weight files...')
                ckpt = wget.download('https://zenodo.org/record/7641552/files/laion_clap_fullset_fusion.pt', os.path.dirname(ckpt))
                # urlretrieve('https://zenodo.org/record/7641552/files/laion_clap_fullset_fusion.pt', ckpt, show_progress)
                print('Download completed!')
        print('Load Checkpoint...')
        ckpt = load_state_dict(ckpt, skip_params=True)
        self.model.load_state_dict(ckpt)
        param_names = [n for n, p in self.model.named_parameters()]
        for n in param_names:
            print(n, "\t", "Loaded" if n in ckpt else "Unloaded")
    
    def get_audio_embedding_from_filelist(self, x):
        """get audio embeddings from the audio file list

        Parameters
        ----------
        x: List[str] (N,): 
            an audio file list to extract features, audio files can have different lengths (as we have the feature fusion machanism)
        
        Returns
        ----------
        audio_embed : numpy.darray (N,D):
            audio embeddings that extracted from audio files
        """ 
        self.model.eval()
        audio_input = []
        for f in x:
            # load the waveform of the shape (T,), should resample to 48000
            audio_waveform, _ = librosa.load(f, sr=48000)           
            # quantize
            audio_waveform = int16_to_float32(float32_to_int16(audio_waveform))
            audio_waveform = torch.from_numpy(audio_waveform).float()
            temp_dict = {}
            # the 'fusion' truncate mode can be changed to 'rand_trunc' if run in unfusion mode
            temp_dict = get_audio_features(
                temp_dict, audio_waveform, 480000, 
                data_truncating='fusion', 
                data_filling='repeatpad',
                audio_cfg=self.model_cfg['audio_cfg']
            )
            audio_input.append(temp_dict)
        audio_embed = self.model.get_audio_embedding(audio_input)
        audio_embed = audio_embed.detach().cpu().numpy()
        return audio_embed


    def get_audio_embedding_from_data(self, x):
        """get audio embeddings from the audio data

        Parameters
        ----------
        x: np.darray (N,T): 
            audio data, must be mono audio tracks.      
        Returns
        ----------
        audio embed: numpy.darray (N,D):
            audio embeddings that extracted from audio files
        """ 
        self.model.eval()
        audio_input = []
        for audio_waveform in x:          
            # quantize
            audio_waveform = int16_to_float32(float32_to_int16(audio_waveform))
            audio_waveform = torch.from_numpy(audio_waveform).float()
            temp_dict = {}
            # the 'fusion' truncate mode can be changed to 'rand_trunc' if run in unfusion mode
            temp_dict = get_audio_features(
                temp_dict, audio_waveform, 480000, 
                data_truncating='fusion', 
                data_filling='repeatpad',
                audio_cfg=self.model_cfg['audio_cfg']
            )
            audio_input.append(temp_dict)
        audio_embed = self.model.get_audio_embedding(audio_input)
        audio_embed = audio_embed.detach().cpu().numpy()
        return audio_embed

    def get_text_embedding(self, x, tokenizer = None):
        """get text embeddings from texts

        Parameters
        ----------
        x: List[str] (N,): 
            text list 
        tokenizer: func:
            the tokenizer function, if not provided (None), will use the default Roberta tokenizer.
        
        Returns
        ----------
        text_embed : numpy.darray (N,D):
            text embeddings that extracted from texts
        """ 
        self.model.eval()
        if tokenizer is not None:
            text_input = tokenizer(x)
        else:
            text_input = self.tokenizer(x)
        text_embed = self.model.get_text_embedding(text_input)
        text_embed = text_embed.detach().cpu().numpy()
        return text_embed
        
    