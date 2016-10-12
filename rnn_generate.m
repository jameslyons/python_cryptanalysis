I = 35;
H = 800; %number of hidden nodes in each hidden layer
O = 26; % number of output classes
LR = 0.0001 ;
momentum = 0.9;

readfrom = 'savednn800small9'
writeto = 'savednn800small9A'
if 1
    load(readfrom);
else
    W1 = randn(I,H)*0.01; b1 = zeros(1,H); W1v = zeros(size(W1)); b1v = zeros(size(b1));
    W2 = randn(H,H)*0.01; b2 = zeros(1,H); W2v = zeros(size(W2)); b2v = zeros(size(b2));
    WF = randn(H,H)*0.01; WFv = zeros(size(WF));
    W3 = randn(H,O)*0.01; b3 = zeros(1,O); W3v = zeros(size(W3)); b3v = zeros(size(b3));
end
sigm = @(x) max(x,0); deriv = @(x) x>0;
load eln500k.mat
load ern500k.mat
f = fopen('J:\\lab_pc\\char_rnn\\eng500k.txt');
instr = fgetl(f);
perror = 0;
acc=0;
count = 0;
bestperp = 100;
fprintf('training \n');
while ischar(instr)
    if count < 250000
        count = count + 1;
        instr = fgetl(f);
        continue
    end
    instr = instr(1:min(length(instr),34));
    input = id2oneofk2(instr(1:end-1),'ABCDEFGHIJKLMNOPQRSTUVWXYZ');
    label = id2oneofk2(instr(2:end),'ABCDEFGHIJKLMNOPQRSTUVWXYZ');
    freqs = mean(id2oneofk2(instr,'ABCDEFGHIJKLMNOPQRSTUVWXYZ'));
    teln = eln(count,:);
    tern = ern(count,:);
    input = [input, label*freqs', [label(2:end,:)*freqs';0], [label(3:end,:)*freqs';0;0],...
        label*teln', [label(2:end,:)*teln';0], [label(3:end,:)*teln';0;0],...
        label*tern', [label(2:end,:)*tern';0], [label(3:end,:)*tern';0;0]];
    
    L = size(input,1);
    a2 = zeros(L,H);
    
    a2prev = zeros(1,H);
    a1 = sigm(bsxfun(@plus,input*(W1+momentum*W1v),(b1+momentum*b1v)));
    for k = 1:L
        a2(k,:) = sigm(a1(k,:)*(W2+momentum*W2v) + a2prev*(WF+momentum*WFv) + (b2+momentum*b2v));
        a2prev = a2(k,:);
    end
    %out = sigm(bsxfun(@plus,a2*(W3+momentum*W3v),(b3+momentum*b3v)));
    out = exp(bsxfun(@plus,a2*(W3+momentum*W3v),(b3+momentum*b3v)));
    out = bsxfun(@rdivide,out,sum(out,2)+eps);
    
    %perror = mean(sum((label-out).^2,2));
    
    % now do back prop over the protein
    err = sign(label - out).*abs(label - out);
    %err(label(:,4)==1,:) = 0;
    delta3 = err;%.*deriv(out);
    W3v = momentum*W3v + 1/L * LR*a2'*delta3;
    b3v = momentum*b3v + LR*mean(delta3,1);
    W3 = W3 + W3v;
    b3 = b3 + b3v;
    
    delta2 = zeros(L,H);
    deltaFnext = zeros(1,H);
    for k = L:-1:1
        delta2(k,:) = (delta3(k,:)*W3' + deltaFnext*WF').*deriv(a2(k,:));
        deltaFnext = delta2(k,:);
    end
    
    % update the weights
    
    WFv = momentum*WFv + 1/L * LR*a2(1:end-1,:)'*delta2(2:end,:);
    WF = WF + WFv;
    
    W2v = momentum*W2v + 1/L * LR*a1'*delta2;
    b2v = momentum*b2v + LR*mean(delta2,1);
    W2 = W2 + W2v;
    b2 = b2 + b2v;
    
    delta1 = (W2*delta2')'.*deriv(a1);
    W1v = momentum*W1v + 1/L * LR*input'*delta1;
    b1v = momentum*b1v + LR*mean(delta1,1);
    W1 = W1 + W1v;
    b1 = b1 + b1v;
    instr = fgetl(f);
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if mod(count,100)==0
        
        correct = 0;
        total = 0;
        tf = fopen('J:\\lab_pc\\char_rnn\\eng10k.txt');
        perp = 0;
        for w = 1:1000
            tinstr = fgetl(tf);
            tinstr = tinstr(1:min(length(tinstr),34));
            input = id2oneofk2(tinstr(1:end-1),'ABCDEFGHIJKLMNOPQRSTUVWXYZ');
            label = id2oneofk2(tinstr(2:end),'ABCDEFGHIJKLMNOPQRSTUVWXYZ');
            freqs = mean(id2oneofk2(tinstr,'ABCDEFGHIJKLMNOPQRSTUVWXYZ'));
            teln = eln(w,:);
            tern = ern(w,:);
            input = [input, label*freqs', [label(2:end,:)*freqs';0], [label(3:end,:)*freqs';0;0],...
                label*teln', [label(2:end,:)*teln';0], [label(3:end,:)*teln';0;0],...
                label*tern', [label(2:end,:)*tern';0], [label(3:end,:)*tern';0;0]];
            
            LL = size(input,1);
            a22 = zeros(LL,H);
            a2prev = zeros(1,H);
            a11 = sigm(bsxfun(@plus,input*W1,b1));
            for k = 1:LL
                a22(k,:) = sigm(a11(k,:)*W2 + a2prev*WF + b2);
                a2prev = a22(k,:);
            end
            %out1 = sigm(bsxfun(@plus,a22*W3,b3));
            out1 = exp(bsxfun(@plus,a22*W3,b3));
            out1 = bsxfun(@rdivide,out1,sum(out1,2)+eps);
            
            %out1 = out1(:,1:3);
            [~,ind1] = max(out1,[],2);
            [~,ind2] = max(label,[],2);
            perp = perp + sum(log(diag(out1(:,ind2))));
            total = total + LL;
            correct = correct + sum(ind1==ind2);
            
        end
        acc = correct/total;
        fprintf('%d: %f (%f,%f)',count,LR,exp(-perp/total),acc);
        
        fclose(tf);
        if exp(-perp/total) < bestperp
            bestperp = exp(-perp/total);
            save(writeto,'W1','W2','W3','b1','b2','b3','WF');
            fprintf(' saved');
        else
            %LR = LR * 0.995;
        end
        fprintf('\n');
        fprintf('%s\n',char(ind2+'A'-1));
        fprintf('%s\n',char(ind1+'A'-1));
        
    end
    count = count + 1;
    %fprintf('\naccuracy = %f\n',acc);
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %LR = LR * 0.9999;
end
fclose(f);
fprintf('\naccuracy = %f\n',acc);


