from torch import nn
from modules.embedding import Embedding
from modules.encoder import Encoder
from modules.decoder import Decoder

class Model(nn.Module):
    def __init__(self, vocabulary, training):
        super(Model, self).__init__()

        self._embedding = Embedding(vocabulary = vocabulary)
        self._encoder = Encoder(embedding = self._embedding, training = training)
        self._decoder = Decoder(embedding = self._embedding, training = training)

    def forward(self, input_seqs, input_lengths, target_seqs, global_step = -1):
        encoder_outputs, encoder_final_hidden_state = self._encoder(input_seqs, input_lengths)
        return self._decoder(encoder_outputs, encoder_final_hidden_state, target_seqs, global_step)


if __name__ == "__main__":
    from data_loading.corpus_loader import CORPUS_FILE, Corpus
    from data_loading.data_tensor_builder import BatchTensorBuilder
    from modules.loss import masked_nll_loss
    corpus = Corpus(CORPUS_FILE)
    tensor_builder = BatchTensorBuilder(corpus.seqs_data[:5], corpus.vocabulary)
    input_seqs = tensor_builder.input_seqs_tensor
    input_lengths = tensor_builder.input_lengths
    target_seqs = tensor_builder.target_seqs_tensor
    model = Model(corpus.vocabulary, training=True)
    decoder_outputs = model(input_seqs, input_lengths, target_seqs, 0)
    step_loss = masked_nll_loss(decoder_outputs, target_seqs, tensor_builder.masks)
    print(step_loss)